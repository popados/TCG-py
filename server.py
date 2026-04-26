"""
Simple TCP room server for the TCG project
- Run: python server.py
- Clients send simple text commands terminated by newline (\n).

Protocol (text lines):
- JOIN <room_id>|<player_name>    -> join specified room
- DECK <fire|water>               -> set player deck, game starts when both set
- PLAY <payload>                  -> play card payload on active player's turn
- ATTACK <damage>                 -> apply commander damage to opponent
- ENDTURN                         -> pass turn to opponent
- LEAVE                           -> leave current room
- QUIT                            -> disconnect

Server messages sent to clients (prefixed by SERVER:):
- SERVER:OK Joined room <room_id>
- SERVER:WAIT Waiting for an opponent...
- SERVER:READY Opponent joined
- SERVER:FORWARD <payload>         (forwarded PLAY from other player)
- SERVER:TURN <player_name>        (active player's turn)
- SERVER:STATUS ...                (commander health, field state, round/mana)
- SERVER:GAMEOVER ...              (winner/ending condition)
- SERVER:INFO <text>

This is minimal and intended for local testing and iterative improvement.
"""

import socket
import sys
import threading
import traceback
import os
import logging
import datetime

HOST = '0.0.0.0'
PORT = 9000

LOGS_DIR = 'server_logs'

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Create a new log file with timestamp
LOG_FILENAME = os.path.join(LOGS_DIR, f"server_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILENAME),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# Pre-create three rooms for clients to join
def make_room():
    return {
        'clients': [],
        'round': 0,
        'mana': 0,
        'game_active': False,
        'current_turn': 0,
        'commander_health': [20, 20],
        'fields': [[], []],
    }


rooms = {
    'room1': make_room(),
    'room2': make_room(),
    'room3': make_room(),
}
rooms_lock = threading.Lock()


def send_line(conn, line):
    try:
        conn.sendall((line + "\n").encode())
    except Exception:
        pass


def remove_client_from_room(conn):
    with rooms_lock:
        for room_id, room in rooms.items():
            clients = room.get('clients', [])
            # clients are dicts with 'conn'
            updated = [c for c in clients if c.get('conn') is not conn]
            if len(updated) != len(clients):
                room['clients'] = updated
                room['game_active'] = False
                room['current_turn'] = 0
                room['commander_health'] = [20, 20]
                room['fields'] = [[], []]
                room['round'] = 0
                room['mana'] = 0
                for cinfo in room['clients']:
                    send_line(cinfo['conn'], "SERVER:INFO Opponent disconnected")


def player_index(room, conn):
    for idx, cinfo in enumerate(room.get('clients', [])):
        if cinfo.get('conn') is conn:
            return idx
    return None


def format_field(field_cards):
    if not field_cards:
        return "Empty"
    return ", ".join(
        f"{c['name']}(ATK:{c['attack']},HP:{c['health']})" for c in field_cards
    )


def broadcast_room(room, line):
    for cinfo in room.get('clients', []):
        send_line(cinfo['conn'], line)


def send_room_status_locked(room_id):
    room = rooms.get(room_id)
    if not room or len(room.get('clients', [])) < 2:
        return
    p1 = room['clients'][0].get('name', 'Player1')
    p2 = room['clients'][1].get('name', 'Player2')
    h1, h2 = room['commander_health']
    f1 = format_field(room['fields'][0])
    f2 = format_field(room['fields'][1])
    turn_name = room['clients'][room['current_turn']].get('name', 'Unknown')
    broadcast_room(room, f"SERVER:STATUS Round {room['round']} Mana {room['mana']}")
    broadcast_room(room, f"SERVER:STATUS {p1} Commander HP: {h1}")
    broadcast_room(room, f"SERVER:STATUS {p2} Commander HP: {h2}")
    broadcast_room(room, f"SERVER:STATUS {p1} Field: {f1}")
    broadcast_room(room, f"SERVER:STATUS {p2} Field: {f2}")
    broadcast_room(room, f"SERVER:STATUS Turn: {turn_name}")


def check_game_over_locked(room_id):
    room = rooms.get(room_id)
    if not room or len(room.get('clients', [])) < 2:
        return False
    h1, h2 = room['commander_health']
    if h1 <= 0 or h2 <= 0:
        if h1 <= 0 and h2 <= 0:
            result = "DRAW"
            msg = "Both commanders reached 0 or less health. Draw game."
        elif h1 <= 0:
            result = room['clients'][1].get('name', 'Player2')
            msg = f"Game Over! {result} wins."
        else:
            result = room['clients'][0].get('name', 'Player1')
            msg = f"Game Over! {result} wins."
        broadcast_room(room, f"SERVER:GAMEOVER {msg}")
        room['game_active'] = False
        return True
    return False


def advance_turn_locked(room_id):
    room = rooms.get(room_id)
    if not room or len(room.get('clients', [])) < 2 or not room.get('game_active'):
        return

    room['current_turn'] = 1 - room['current_turn']
    if room['current_turn'] == 0:
        room['round'] += 1
        room['mana'] += 1

    # Send status first so the client has updated round/mana before receiving the turn signal
    send_room_status_locked(room_id)
    turn_name = room['clients'][room['current_turn']].get('name', 'Unknown')
    broadcast_room(room, f"SERVER:TURN {turn_name}")


def start_game_if_ready_locked(room_id):
    room = rooms.get(room_id)
    if not room or len(room.get('clients', [])) != 2:
        return
    if room['game_active']:
        return
    if not all(c.get('deck') in ('FIRE', 'WATER') for c in room['clients']):
        return

    room['round'] = 1
    room['mana'] = 1
    room['game_active'] = True
    room['current_turn'] = 0
    room['commander_health'] = [20, 20]
    room['fields'] = [[], []]

    broadcast_room(room, "SERVER:READY Opponent joined")
    # Send full status before the turn signal so clients have round/mana when they receive SERVER:TURN
    send_room_status_locked(room_id)
    turn_name = room['clients'][room['current_turn']].get('name', 'Unknown')
    broadcast_room(room, f"SERVER:TURN {turn_name}")


def client_thread(conn, addr):
    print(f"Client connected: {addr}")
    room_id = None
    player_name = None
    try:
        with conn:
            buf = b""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buf += data
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    try:
                        line = line.decode().strip()
                    except Exception:
                        line = ""
                    if not line:
                        continue

                    parts = line.split(" ", 1)
                    cmd = parts[0].upper()
                    arg = parts[1] if len(parts) > 1 else ""

                    # Global turn lock: while a game is active in the room,
                    # only the active-turn player may send turn-phase commands.
                    # Allow LEAVE/QUIT so a player can always exit.
                    if room_id and cmd not in ('LEAVE', 'QUIT'):
                        with rooms_lock:
                            room = rooms.get(room_id)
                            if room and room.get('game_active'):
                                idx = player_index(room, conn)
                                if idx is not None and idx != room.get('current_turn', 0):
                                    active_name = room['clients'][room['current_turn']].get('name', 'active player')
                                    send_line(conn, f"SERVER:LOCKED Command blocked. Wait for {active_name} to finish turn")
                                    continue

                    if cmd == 'JOIN':
                        # arg format: room_id|player_name
                        if '|' in arg:
                            rid, pname = arg.split('|', 1)
                            rid = rid.strip()
                            pname = pname.strip()
                        else:
                            rid = arg.strip()
                            pname = f"Player{addr[1]}"

                        with rooms_lock:
                            room = rooms.get(rid)
                            if room is None:
                                send_line(conn, f"SERVER:INFO Room {rid} is not available")
                                continue
                            if len(room['clients']) >= 2:
                                send_line(conn, f"SERVER:INFO Room {rid} is full")
                                continue

                            room['clients'].append({'conn': conn, 'name': pname, 'deck': None})
                            room_id = rid
                            player_name = pname
                            send_line(conn, f"SERVER:OK Joined room {rid}")
                            if len(room['clients']) == 1:
                                send_line(conn, "SERVER:WAIT Waiting for an opponent...")
                            else:
                                broadcast_room(room, "SERVER:READY Opponent joined")
                                broadcast_room(room, "SERVER:INFO Select your deck with 1/2 in client, then send DECK")

                    elif cmd == 'DECK':
                        if not room_id:
                            send_line(conn, "SERVER:INFO Not in a room")
                            continue
                        deck_choice = arg.strip().upper()
                        if deck_choice not in ('FIRE', 'WATER'):
                            send_line(conn, "SERVER:INFO Invalid deck choice")
                            continue

                        with rooms_lock:
                            room = rooms.get(room_id)
                            if not room:
                                send_line(conn, "SERVER:INFO Room not found")
                                continue
                            if room.get('game_active'):
                                send_line(conn, "SERVER:INFO Cannot change deck after game start")
                                continue
                            idx = player_index(room, conn)
                            if idx is None:
                                send_line(conn, "SERVER:INFO Not registered in room")
                                continue
                            room['clients'][idx]['deck'] = deck_choice
                            logger.info("%s selected %s deck in %s", room['clients'][idx]['name'], deck_choice, room_id)
                            send_line(conn, f"SERVER:INFO Deck set to {deck_choice}")
                            if len(room['clients']) == 2:
                                other_idx = 1 - idx
                                send_line(room['clients'][other_idx]['conn'], f"SERVER:INFO Opponent selected {deck_choice}")
                            start_game_if_ready_locked(room_id)

                    elif cmd == 'PLAY':
                        if not room_id:
                            send_line(conn, "SERVER:INFO Not in a room")
                            continue
                        with rooms_lock:
                            room = rooms.get(room_id)
                            if not room or len(room['clients']) < 2:
                                send_line(conn, "SERVER:INFO Room not ready")
                                continue
                            if not room['game_active']:
                                send_line(conn, "SERVER:INFO Game not active yet")
                                continue
                            idx = player_index(room, conn)
                            if idx is None:
                                send_line(conn, "SERVER:INFO Not registered in room")
                                continue
                            if idx != room['current_turn']:
                                send_line(conn, "SERVER:INFO Not your turn")
                                continue

                            for cinfo in room['clients']:
                                if cinfo['conn'] is not conn:
                                    send_line(cinfo['conn'], f"SERVER:FORWARD {arg}")

                            payload = arg.strip().split()
                            # Expected CARD payload: CARD <idx> <name> <type> <attack> <health> <cost>
                            if len(payload) >= 7 and payload[0].upper() == 'CARD':
                                card_name = payload[2]
                                card_type = payload[3]
                                try:
                                    attack = int(payload[4])
                                    health = int(payload[5])
                                except ValueError:
                                    attack = 0
                                    health = 0
                                if card_type.lower() == 'creature':
                                    room['fields'][idx].append({
                                        'name': card_name,
                                        'attack': attack,
                                        'health': health,
                                    })
                                    broadcast_room(room, f"SERVER:INFO {room['clients'][idx]['name']} summoned {card_name}")
                                    send_room_status_locked(room_id)

                            send_line(conn, "SERVER:INFO Played")

                    elif cmd == 'ATTACK':
                        if not room_id:
                            send_line(conn, "SERVER:INFO Not in a room")
                            continue
                        with rooms_lock:
                            room = rooms.get(room_id)
                            if not room or len(room['clients']) < 2:
                                send_line(conn, "SERVER:INFO Room not ready")
                                continue
                            if not room['game_active']:
                                send_line(conn, "SERVER:INFO Game not active")
                                continue
                            idx = player_index(room, conn)
                            if idx is None:
                                send_line(conn, "SERVER:INFO Not registered in room")
                                continue
                            if idx != room['current_turn']:
                                send_line(conn, "SERVER:INFO Not your turn")
                                continue
                            try:
                                damage = int(arg.strip())
                            except ValueError:
                                send_line(conn, "SERVER:INFO Invalid ATTACK damage")
                                continue
                            defender = 1 - idx
                            room['commander_health'][defender] -= damage
                            attacker_name = room['clients'][idx]['name']
                            defender_name = room['clients'][defender]['name']
                            broadcast_room(room, f"SERVER:INFO {attacker_name} attacked {defender_name}'s commander for {damage}")
                            if not check_game_over_locked(room_id):
                                # An attack ends the active player's turn.
                                advance_turn_locked(room_id)

                    elif cmd == 'ENDTURN':
                        if not room_id:
                            send_line(conn, "SERVER:INFO Not in a room")
                            continue
                        with rooms_lock:
                            room = rooms.get(room_id)
                            if not room or len(room['clients']) < 2:
                                send_line(conn, "SERVER:INFO Room not ready")
                                continue
                            if not room['game_active']:
                                send_line(conn, "SERVER:INFO Game not active")
                                continue
                            idx = player_index(room, conn)
                            if idx is None:
                                send_line(conn, "SERVER:INFO Not registered in room")
                                continue
                            if idx != room['current_turn']:
                                send_line(conn, "SERVER:INFO Not your turn")
                                continue
                            advance_turn_locked(room_id)

                    elif cmd == 'LEAVE':
                        if room_id:
                            with rooms_lock:
                                room = rooms.get(room_id)
                                if room:
                                    room['clients'] = [x for x in room['clients'] if x['conn'] is not conn]
                                    room['game_active'] = False
                                    room['current_turn'] = 0
                                    room['commander_health'] = [20, 20]
                                    room['fields'] = [[], []]
                                    room['round'] = 0
                                    room['mana'] = 0
                                    for cinfo in room['clients']:
                                        send_line(cinfo['conn'], "SERVER:INFO Opponent left the room")
                            room_id = None
                            player_name = None
                            send_line(conn, "SERVER:INFO Left room")

                    elif cmd == 'QUIT':
                        send_line(conn, "SERVER:INFO Bye")
                        return

                    else:
                        send_line(conn, "SERVER:INFO Unknown command")
    except Exception:
        traceback.print_exc()
    finally:
        remove_client_from_room(conn)
        print(f"Client disconnected: {addr}")


def main():
    print(f"Starting server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        # event to signal shutdown (from Ctrl+C or admin command)
        shutdown_event = threading.Event()

        # start host display thread
        def host_display_loop():
            try:
                while True:
                    with rooms_lock:
                        print('\n--- Server Rooms Status --- %s ---' % datetime.datetime.now().strftime('%m/%d/%Y:%H:%M:%S'))
                        for rid, room in rooms.items():
                            names = [c.get('name') for c in room.get('clients', [])]
                            print(f"{rid}: {len(names)}/2 connected - {names}")
                        print('---------------------------\n')
                    # sleep without importing time at top (use threading.Event)
                    threading.Event().wait(3.0)
            except Exception:
                pass

        host_thread = threading.Thread(target=host_display_loop, daemon=True)
        host_thread.start()

        # admin input thread: type 'quit' or 'exit' to stop the server
        def admin_input_loop():
            try:
                while not shutdown_event.is_set():
                    cmd = input()
                    if not cmd:
                        continue
                    cmd = cmd.strip().lower()
                    if cmd in ('quit', 'exit'):
                        print('Admin requested shutdown...')
                        shutdown_event.set()
                        break
            except EOFError:
                return
            except Exception:
                return

        admin_thread = threading.Thread(target=admin_input_loop, daemon=True)
        admin_thread.start()

        try:
            s.settimeout(1.0)
            while not shutdown_event.is_set():
                try:
                    conn, addr = s.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break
                t = threading.Thread(target=client_thread, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            shutdown_event.set()

        # perform shutdown actions
        print('\nServer shutting down. Notifying clients...')
        with rooms_lock:
            for rid, room in rooms.items():
                for cinfo in list(room.get('clients', [])):
                    try:
                        send_line(cinfo['conn'], 'SERVER:INFO Server shutting down')
                        try:
                            cinfo['conn'].shutdown(socket.SHUT_RDWR)
                        except Exception:
                            pass
                        cinfo['conn'].close()
                    except Exception:
                        pass
                room['clients'] = []
        return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    sys.exit(0)
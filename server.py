"""
Simple TCP room server for the TCG project
- Run: python server.py
- Clients send simple text commands terminated by newline (\n).

Protocol (text lines):
- JOIN <room_id>|<player_name>    -> join specified room
- PLAY <payload>                  -> server forwards to the other player in room
- LEAVE                           -> leave current room
- QUIT                            -> disconnect

Server messages sent to clients (prefixed by SERVER:):
- SERVER:OK Joined room <room_id>
- SERVER:WAIT Waiting for an opponent...
- SERVER:READY Opponent joined
- SERVER:FORWARD <payload>   (forwarded PLAY from other player)
- SERVER:INFO <text>

This is minimal and intended for local testing and iterative improvement.
"""

import socket
import sys
import threading
import traceback

HOST = '0.0.0.0'
PORT = 9000

# Pre-create three rooms for clients to join
rooms = {
    'room1': {'clients': [], 'round': 0, 'mana': 0},
    'room2': {'clients': [], 'round': 0, 'mana': 0},
    'room3': {'clients': [], 'round': 0, 'mana': 0},
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
            room['clients'] = [c for c in clients if c.get('conn') is not conn]


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
                            # only allow joining pre-created rooms
                            room = rooms.get(rid)
                            if room is None:
                                send_line(conn, f"SERVER:INFO Room {rid} is not available")
                                continue
                            clients = room['clients']
                            if len(clients) >= 2:
                                send_line(conn, f"SERVER:INFO Room {rid} is full")
                                continue
                            client_info = {'conn': conn, 'name': pname, 'ended': False, 'deck': None}
                            clients.append(client_info)
                            room_id = rid
                            player_name = pname
                            send_line(conn, f"SERVER:OK Joined room {rid}")
                            if len(clients) == 1:
                                send_line(conn, "SERVER:WAIT Waiting for an opponent...")
                            elif len(clients) == 2:
                                # initialize round state
                                room['round'] = 1
                                room['mana'] = 1
                                for cinfo in clients:
                                    send_line(cinfo['conn'], "SERVER:READY Opponent joined")
                                    send_line(cinfo['conn'], f"SERVER:ROUND {room['round']} MANA: {room['mana']}")

                        # Handle deck selection
                        if not room_id:
                            send_line(conn, "SERVER:INFO Not in a room")
                            continue
                        deck_choice = arg.strip().upper()
                        if deck_choice not in ['FIRE', 'WATER']:
                            send_line(conn, "SERVER:INFO Invalid deck choice")
                            continue
                        with rooms_lock:
                            room = rooms.get(room_id)
                            if not room:
                                send_line(conn, "SERVER:INFO Room not found")
                                continue
                            # Find this client and update their deck
                            for cinfo in room['clients']:
                                if cinfo['conn'] is conn:
                                    cinfo['deck'] = deck_choice
                                    print(f"[SERVER] {cinfo['name']} selected {deck_choice} deck in room {room_id}")
                                    break
                            # Notify all clients in the room about the deck selection
                            # for cinfo in room['clients']:
                            #     send_line(cinfo['conn'], f"SERVER:INFO {player_name} selected {deck_choice} deck")
                    elif cmd == 'PLAY':
                        # forward to other client in room
                        if not room_id:
                            send_line(conn, "SERVER:INFO Not in a room")
                            continue
                        with rooms_lock:
                            room = rooms.get(room_id)
                            if not room:
                                send_line(conn, "SERVER:INFO Room not found")
                                continue
                            for cinfo in room['clients']:
                                if cinfo['conn'] is not conn:
                                    send_line(cinfo['conn'], f"SERVER:FORWARD {arg}")
                            # optionally acknowledge
                            send_line(conn, "SERVER:INFO Played")
                    elif cmd == 'ENDTURN':
                        # mark this player's end turn status; when both ended, advance round
                        if not room_id:
                            send_line(conn, "SERVER:INFO Not in a room")
                            continue
                        with rooms_lock:
                            room = rooms.get(room_id)
                            if not room:
                                send_line(conn, "SERVER:INFO Room not found")
                                continue
                            # find client
                            for cinfo in room['clients']:
                                if cinfo['conn'] is conn:
                                    cinfo['ended'] = True
                            # notify other
                            for cinfo in room['clients']:
                                if cinfo['conn'] is not conn:
                                    send_line(cinfo['conn'], f"SERVER:INFO Opponent ended turn")
                            # check if all ended
                            all_ended = all(ci['ended'] for ci in room['clients']) and len(room['clients']) == 2
                            if all_ended:
                                room['round'] += 1
                                room['mana'] += 1
                                # reset ended flags
                                for ci in room['clients']:
                                    ci['ended'] = False
                                    send_line(ci['conn'], f"SERVER:NEW ROUND {room['round']} {room['mana']}")
                    elif cmd == 'LEAVE':
                        if room_id:
                            with rooms_lock:
                                room = rooms.get(room_id)
                                if room:
                                    room['clients'] = [x for x in room['clients'] if x['conn'] is not conn]
                                    if room['clients']:
                                        for cinfo in room['clients']:
                                            send_line(cinfo['conn'], "SERVER:INFO Opponent left the room")
                                    else:
                                        rooms.pop(room_id, None)
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
                        print('\n--- Server Rooms Status ---')
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
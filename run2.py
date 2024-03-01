from library import Player
from library import RFID
from library import Ports
from library import Misc

p = Ports.Ports()
p.print(detail=True)

folder = 'songs'
player = Player.MP3Player(folder)

reader = RFID.get_rfid_reader('/dev/ttyUSB0')

pause_antenna = 1
play_antenna = 2
output_file = 'output.txt'

file = open(output_file, "w")
file.close()

while True:
    stream = reader.readlines()
    records = RFID.convert_stream_to_records(stream)
    antennas, events, box_times = RFID.get_antenna_events(records)
    tags = RFID.process_antenna_events(antennas, events)

    if 'arrived 1' in tags or 'arrived 2' in tags:
        if f'arrived {play_antenna}' in tags:
            player.pause()
            player_message = player.last_message
        if f'arrived {pause_antenna}' in tags:
            if not player.currently_playing: player.start()
            if player.currently_playing: player.resume()
            player_message = player.last_message

        time_stamp = box_times[-1]
        current_tag = tags[-1]
        output_list = [time_stamp, current_tag, player_message]
        output = Misc.concatenate(output_list)
        print(output)
        file = open(output_file, "a")
        file.write(output + '\n')
        file.close()





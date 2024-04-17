from library import Player
from library import RFID
from library import Ports
from library import Misc

p = Ports.Ports()
p.print(detail=True)

folder = 'songs'
player = Player.MP3Player(folder)

reader = RFID.get_rfid_reader('COM4')

play_music = True #Set this to True to play music
pause_antenna = 1 #set the antenna number that you want to PAUSE Music here ..this is what you need to change to reflect the antenna to PLAY or PAUSE
play_antenna = 2  # Set the antenna number that you want to PLAY music here

output_file = Misc.generate_csv_filename()
file = open(output_file, "w")
file.close()
player_message = None
while True:
    stream = reader.readlines()
    if len(stream)>0: print(stream)
    records = RFID.convert_stream_to_records(stream)
    antennas, events, box_times = RFID.get_antenna_events(records)
    tags = RFID.process_antenna_events(antennas, events)

    if 'arrived 1' in tags or 'arrived 2' in tags:
        if f'arrived {play_antenna}' in tags:
            if play_music:
                player.pause()
                player_message = player.last_message
        if f'arrived {pause_antenna}' in tags:
            if play_music:
                if not player.currently_playing: player.start()
                if player.currently_playing: player.resume()
                player_message = player.last_message

        raspberry_pi_time = Player.get_time_stamp()
        time_stamp = box_times[-1]
        current_tag = tags[-1]
        output_list = [time_stamp, current_tag, player_message, play_music, raspberry_pi_time, str(tags)]
        output = Misc.concatenate(output_list)
        print(output)
        file = open(output_file, "a")
        file.write(output + '\n')
        file.close()





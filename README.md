# Christmas Lights

Turn any WAV file into a christmas light show. Inspired by the classic: https://www.youtube.com/watch?v=pWBjl-jPcVM. Supports playing the show in a pygame simulator, with Raspberry Pi support coming soon via GPIO.

To run the christmas light show (pygame simulator for now):
`poetry run python christmas_lights/run.py <wav_file_name>`
Where you have an accompanying WAV file at: `data/<wav_file_name>.wav`

If you have an MP3 file, but not a WAV file, then:
`poetry run python christmas_lights/mp3_to_wav.py <mp3_file_name>`
Will read an MP3 file at `data/<mp3_file_name>.mp3` and create a WAV file at `data/<mp3_file_name>.wav`

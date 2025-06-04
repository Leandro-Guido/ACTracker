import argparse
import subprocess

parser = argparse.ArgumentParser(description="Divide um video em 12 partes usando FFmpeg.")
parser.add_argument('--input', type=str, required=True, help='Caminho para o arquivo de video')
args = vars(parser.parse_args())

input_file = args['input']

def get_duration(filename):
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        filename
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

duration = get_duration(input_file)
part_duration = duration / 12
name_without_ext = input_file.rsplit('.', 1)[0]

for i in range(12):
    start_time = i * part_duration
    output_file = f"{name_without_ext}/parte_{i+1:02d}.mp4"

    cmd = [
        'ffmpeg', '-y', '-ss', str(start_time), '-i', input_file,
        '-t', str(part_duration), '-c', 'copy', output_file
    ]

    subprocess.run(cmd)

print("corte concluido.")

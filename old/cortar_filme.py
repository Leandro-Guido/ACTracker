import subprocess

PASTA_CORTES = "cortes"

def get_duration(filename):
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        filename
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def cortar_em_partes(input_file, partes):
    if partes < 2:
        return

    duration = get_duration(input_file)
    part_duration = duration / partes
    name_without_ext = input_file.rsplit('.', 1)[0]

    for i in range(partes):
        start_time = i * part_duration
        output_file = f"{PASTA_CORTES}/{name_without_ext}/parte_{i+1:02d}.mp4"

        cmd = [
            'ffmpeg', '-y', '-ss', str(start_time), '-i', input_file,
            '-t', str(part_duration), '-c', 'copy', output_file
        ]

        subprocess.run(cmd)

    print("corte concluido.")

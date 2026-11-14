#!/usr/bin/env python3
"""Pipeline de video gratis: cortar, juntar, legendar e comprimir com ffmpeg.

Nenhum servico de nuvem. Gera MP4 H.264 pronto para publicar.
"""
import subprocess, sys, pathlib


def run(cmd):
    print("+", " ".join(cmd[:6]), "...")
    subprocess.run(cmd, check=True, capture_output=True)


def clip(src, dst, start, dur, w=1920, h=1080):
    """Corta um trecho e normaliza para 1080p 30fps."""
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30")
    run(["ffmpeg", "-y", "-ss", str(start), "-i", src, "-t", str(dur),
         "-vf", vf, "-c:v", "libx264", "-crf", "20", "-preset", "medium",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", dst])


def burn_subs(src, dst, srt):
    """Queima legenda .srt no video."""
    run(["ffmpeg", "-y", "-i", src, "-vf",
         f"subtitles={srt}:force_style='FontSize=22,Outline=1'",
         "-c:v", "libx264", "-crf", "20", "-c:a", "copy", dst])


def concat(parts, dst):
    """Junta varios MP4 em um so."""
    lst = pathlib.Path("concat.txt")
    lst.write_text("".join(f"file '{pathlib.Path(p).resolve()}'\n" for p in parts))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", dst])
    lst.unlink()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("exemplos:")
        print("  pipeline.py clip entrada.mp4 saida.mp4 00:00:10 20")
        print("  pipeline.py subs in.mp4 out.mp4 legenda.srt")
        raise SystemExit(1)
    verb = sys.argv[1]
    if verb == "clip":
        clip(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]))
    elif verb == "subs":
        burn_subs(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("verbo desconhecido:", verb)

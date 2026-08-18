import asyncio, edge_tts
from pathlib import Path

OUT = Path(__file__).parent / "assets" / "narration"
OUT.mkdir(parents=True, exist_ok=True)

VOICE = "zh-TW-YunJheNeural"
RATE = "-6%"
PITCH = "-1Hz"

SCRIPT = [
    (1,  "差點被親哥哥殺死？這絕對是史上最驚險的作詩挑戰！"),
    (2,  "三國時期，魏國的曹丕當上了皇帝。但他嫉妒弟弟曹植的絕世才華，一心想要除掉他。"),
    (3,  "在大殿上，曹丕命令曹植：「限你走完七步之內，寫出一首詩，否則立刻處斬！」"),
    (4,  "而且，詩的主題是「兄弟」，但字面裡卻不能出現任何「兄」或「弟」字！"),
    (5,  "曹植深吸一口氣，開始在大殿上邁出第一步。每一步，都是生與死的邊緣。"),
    (6,  "就在走到第七步時，他高聲吟誦出：「煮豆燃豆萁，豆在釜中泣。」"),
    (7,  "「本是同根生，相煎何太急！」"),
    (8,  "他用豆萁燃燒和豆子在鍋裡哭泣作比喻，它們同是根部所生，為什麼要互相煎熬呢？"),
    (9,  "曹丕聽完，感到無比羞愧，當場流下了眼淚，最終放了曹植一條生路。"),
    (10, "這首詩留下了深刻的文學啟示：它不只是一次絕境中的才華展現，更是一聲對手足相殘的痛心控訴。"),
    (11, "本是同根生，相煎何太急。珍惜身邊的親人，別讓嫉妒和競爭傷害了最珍貴的手足感情！")
]

async def synth(i, text):
    out = OUT / f"page-{i:02d}.mp3"
    c = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    await c.save(str(out))
    print(f"OK page-{i:02d}.mp3")

async def main():
    for i, t in SCRIPT:
        for r in range(3):
            try:
                await synth(i, t); break
            except Exception as e:
                print(f"retry {i} ({r+1}): {e}")
                await asyncio.sleep(2)
    print("All done.")

if __name__ == "__main__":
    asyncio.run(main())

import os, pathlib, subprocess, json
from PIL import Image, ImageDraw, ImageFont
out=pathlib.Path("out"); out.mkdir(exist_ok=True)
def run(*args):
    subprocess.run(args,check=True)
def duration(path):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)]))
lessons=[
("What is Flutter?", "flutter --version\nflutter doctor", "Flutter is a user interface toolkit. Dart is the language we write. Widgets describe the interface. A widget tree combines smaller pieces into a screen. Flutter doctor checks your installation. Look at its output and identify any missing Android tools. A successful doctor check does not guarantee every application will compile."),
("Create your application", "flutter create counter_lesson\ncd counter_lesson\nflutter run", "Create a project using the Flutter command line. Open the folder in your editor. The lib main Dart file is the application entry point. Pubspec yaml declares dependencies and assets. Flutter run starts an application on a connected device. This example is a code walkthrough, not a recording of an emulator."),
("Dart functions", "int add(int a, int b) {\n  return a + b;\n}\nvoid main() {\n  print(add(2, 3));\n}", "Dart supports typed parameters and return values. The add function accepts two integers and returns their sum. The main function calls add and prints five. Change the numbers and predict the output. A final variable can only be assigned once. Use descriptive names and small functions."),
("First Flutter screen", "import 'package:flutter/material.dart';\nvoid main() => runApp(const MaterialApp(\n  home: Scaffold(\n    body: Center(child: Text('Hello Flutter')),\n  ),\n));", "RunApp receives the root widget. MaterialApp supplies material design behavior. Scaffold provides a page structure. Center positions its child in the middle. Text displays words. Read the widget tree from outside to inside. Notice the const keyword and trailing commas. Try changing the greeting."),
("Layout widgets", "Column(\n  mainAxisAlignment: MainAxisAlignment.center,\n  children: const [\n    Text('Welcome'),\n    SizedBox(height: 16),\n    Text('Learn Flutter'),\n  ],\n)", "Column arranges children vertically. Row arranges them horizontally. SizedBox creates a fixed gap. Main axis alignment controls positioning along the main axis. The children property accepts a list of widgets. Experiment with different alignment values and predict what happens."),
("Stateful widget", "class Counter extends StatefulWidget {\n  const Counter({super.key});\n  @override\n  State<Counter> createState() => _CounterState();\n}", "A stateless widget describes its interface using inputs. A stateful widget has a state object that can hold changing values. CreateState constructs that object. Here we create a Counter widget. The underscore makes the state class private to its library. Next we will implement it."),
("Build the counter", "class _CounterState extends State<Counter> {\n  int count = 0;\n  @override\n  Widget build(BuildContext context) => Scaffold(\n    body: Center(child: Text('$count')),\n    floatingActionButton: FloatingActionButton(\n      onPressed: () => setState(() => count++),\n      child: const Icon(Icons.add),\n    ),\n  );\n}", "The counter starts at zero. The build method creates a scaffold. The text interpolates the current count. The floating action button calls setState, which schedules a rebuild. Each tap increments the count. Combine this class with the previous declaration and set MaterialApp home to Counter. Trace three button presses."),
("Debug and practice", "flutter analyze\nflutter test\nflutter run", "Analyze reports static issues. Tests check expected behavior. Run launches the app. Try adding a second button that resets the count to zero. Try adding a decrement button. Decide whether negative numbers should be allowed. Explain your decision. Review the difference between a widget and its state. In the next lesson we can explore forms and validation.")
]
font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
mono="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
clips=[]
for i,(title,code,script) in enumerate(lessons):
    img=Image.new("RGB",(1280,720),"#101c2e"); d=ImageDraw.Draw(img)
    d.text((60,35),"MSS TECH ACADEMY  /  FLUTTER BEGINNER",font=ImageFont.truetype(font,24),fill="#69d7ff")
    d.text((60,100),title,font=ImageFont.truetype(font,48),fill="white")
    d.rounded_rectangle((50,190,1230,625),radius=18,fill="#17283e")
    for j,line in enumerate(code.splitlines()):
        d.text((75,210+j*34),line,font=ImageFont.truetype(mono,24),fill="#e4f2ff")
    d.text((60,660),f"LESSON 01  |  CHAPTER {i+1}/{len(lessons)}  |  Narrated code walkthrough",font=ImageFont.truetype(font,22),fill="#69d7ff")
    png=out/f"{i}.png"; img.save(png)
    wav=out/f"{i}.wav"
    run("espeak-ng","-v","en-us","-s","135","-w",str(wav),script)
    # Deliberate practice time for learners; not continuous narration.
    seconds=max(78,duration(wav)+5)
    clip=out/f"{i}.mp4"
    run("ffmpeg","-y","-loglevel","error","-loop","1","-framerate","24","-i",str(png),"-i",str(wav),"-af","apad","-t",str(seconds),"-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","-c:a","aac","-ar","44100",str(clip))
    clips.append(clip)
manifest=out/"concat.txt"; manifest.write_text("".join(f"file '{p.name}'\n" for p in clips))
final=out/"flutter-lesson-01.mp4"
run("ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(manifest),"-c","copy",str(final))
length=duration(final)
assert 600<=length<=1200,length
print(json.dumps({"duration_seconds":length,"file":str(final),"narration":"espeak-ng","visuals":"code cards; no live emulator"},indent=2))

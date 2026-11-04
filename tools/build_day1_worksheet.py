"""Build the concise English A4 portrait Day 1 practical guide.

Requires reportlab and Pillow. No hardware is accessed. The script regenerates
both the Markdown source and PDF; edit the CONTENT below before rebuilding.
"""
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether

ROOT=Path(__file__).resolve().parents[1]
FIGS=ROOT/'training_materials'/'figs'
OUT=ROOT/'output'/'pdf'/'Day_01_Quick_Tutorials_Portrait.pdf'
SOURCE=ROOT/'training_materials'/'worksheets'/'Day_01_Quick_Tutorials_Worksheet.md'

CONTENT=[
 dict(title='LabVIEW quick tutorial 1', topic='Plot random values', image='LV_01_demo_loops.jpg',
 goal='Create parallel loops to display individual samples on a chart and a batch of samples on a graph.',
 caption='Upper loop: one sample per chart update. Lower loop: 100 samples per graph update.',
 groups=[
 ('Create a new VI',[
 'Open LabVIEW and create a Blank VI on My Computer. Save it as QT1_Random_Display.vi.',
 'Use Ctrl+E to switch between the Front Panel and Block Diagram.',
 'On the Front Panel, select View > Controls Palette. On the Block Diagram, select View > Functions Palette. Pin the palettes open if needed.',
 'Use Ctrl+H to display Context Help. Use Search in the palette when a block is difficult to find.'
 ]),
 ('Build the loop for individual samples',[
 'On the Block Diagram, find While Loop in the Structures group. Select it and drag a rectangular loop boundary.',
 'Click Search in the Functions Palette. Search for Random and place Random Number (0-1) inside the loop.',
 'On the Front Panel, find Waveform Chart in the Graph or Graphs group. Place the chart, then return to the Block Diagram.',
 'Move the chart terminal inside the While Loop. Use the Wiring tool to connect Random Number (0-1) to the chart terminal.',
 'Search for Time Delay and place it inside the loop. Set the delay to 0.10 s for this exercise.',
 'Right-click the loop condition terminal and create a Boolean control. Name it loop_chart and use Stop if True.'
 ]),
 ('Build the loop for a batch of samples',[
 'Create a second While Loop below the first one. Place a For Loop inside it.',
 'Right-click the For Loop N terminal, create a numeric constant and enter 100.',
 'Place Random Number (0-1) and Wait (ms) inside the For Loop. Create a constant of 10 for the Wait input.',
 'On the Front Panel, add a Waveform Graph. Place its diagram terminal outside the For Loop but inside the second While Loop.',
 'Wire the random value through the For Loop boundary to the graph. Right-click the output tunnel and enable indexing so it produces a 1D array.',
 'Create a separate Boolean control for the outer While Loop condition. Name it loop_graph.'
 ]),
 ('Run and adjust the VI',[
 'Click Run. The chart updates one value at a time; the graph updates after each 100-sample batch.',
 'Change the chart delay to 0.20 s and run again. Notice the slower chart update rate.',
 'Stop loop_chart and confirm that loop_graph continues. Stop the second loop; it may finish its current For Loop batch first.',
 'Save the VI. Use the Stop controls during normal operation rather than Abort Execution.'
 ])],
 note='Palette group names vary by LabVIEW version. Search by the function name if the illustrated group is unavailable. A plain array graph displays sample indices unless its axis is configured for time.'),
 dict(title='LabVIEW quick tutorial 2', topic='Build a moving average', image='LV_01_demo_MA.jpg',
 goal='Use a shift register, arithmetic and a SubVI to smooth the chart data.',
 caption='The upper loop shows a three-point moving average. The lower graph loop is unchanged.',
 groups=[
 ('Prepare the VI',[
 'Open QT1_Random_Display.vi and save a copy as QT2_Moving_Average.vi.',
 'Keep the lower graph loop unchanged. Work on the upper chart loop.'
 ]),
 ('Store the previous samples',[
 'Right-click the upper While Loop boundary and select Add Shift Register.',
 'Expand the left shift-register terminal downward to expose two previous values, as shown in the reference figure.',
 'Wire the current random value to the right shift-register terminal.',
 'For repeatable startup, create a zero constant outside the loop for each left terminal. This initialization is added for this exercise.'
 ]),
 ('Calculate the average',[
 'Search for Compound Arithmetic. Place it inside the loop and configure it for addition with three inputs.',
 'Wire the current value and the two previous values to the three inputs.',
 'Search for Divide. Wire the sum to its numerator and a constant of 3 to its denominator.',
 'The output is the mean of the current sample and the two previous samples.'
 ]),
 ('Display raw and filtered values',[
 'Search for Bundle. Configure it with two inputs: the raw sample and the average.',
 'Wire the resulting two-element cluster to the Waveform Chart.',
 'Run the VI. Use the chart plot legend to give the traces different names and colors.',
 'Notice the smoother trace and its delay. Zero initialization affects the first two average values.'
 ]),
 ('Create and reuse a SubVI',[
 'Stop both loops. Select only the addition and division code, leaving the shift register in the main VI.',
 'Select Edit > Create SubVI, or create a blank SubVI manually. Save it as MA3_Calculate.vi.',
 'Assign connector-pane inputs for current, previous_1 and previous_2, and an output for mean. Create a readable icon.',
 'Reconnect the SubVI in the main loop. Confirm the input and output assignments using Context Help.',
 'Try inputs 1, 2 and 3 in the SubVI: the mean should be 2. Run the main VI again and save both files.'
 ])],
 note='The reference figure implements three points. To extend it to N points, store only the latest N samples and define how the filter handles startup.'),
 dict(title='LabVIEW quick tutorial 3', topic='Control parallel loops from the UI', image='LV_01_demo_sync.jpg',
 goal='Use an Event Structure and a notifier to stop both worker loops with one UI control.',
 caption='Top: UI event loop. Middle: chart loop. Bottom: graph loop. One notifier carries the shared Stop request.',
 groups=[
 ('Prepare the shared Stop control',[
 'Open QT2_Moving_Average.vi and save a copy as QT3_UI_Stop.vi.',
 'Add a Boolean Stop button on the Front Panel. Name it all_loops.',
 'Search for Obtain Notifier. Place it before the loops and wire a Boolean False constant to the element data type input.',
 'Branch the notifier reference to the UI loop and both worker loops.'
 ]),
 ('Build the UI event loop',[
 'Create a third While Loop above the worker loops. Place an Event Structure inside it.',
 'Right-click the Event Structure boundary and add the all_loops: Value Change event.',
 'Place the all_loops terminal inside its event case. This also allows a latch-action button to reset when read.',
 'Search for Send Notification. In the event case, wire the notifier reference and send True as the notification.',
 'Arrange for the UI loop to stop after handling this event. Do not place the acquisition code inside the event case.'
 ]),
 ('Receive Stop in both worker loops',[
 'Search for Wait on Notification. Place one instance inside each worker loop and wire the shared notifier reference.',
 'Set timeout in ms to 10. Set ignore previous to False so a Stop sent before the wait can still be received.',
 'Wire a received True to each worker loop Stop condition. Combine it with an existing local Stop control using OR if that control is retained.',
 'Continue running on an ordinary timeout. Treat an actual notifier error separately from a timeout.',
 'Use Context Help to confirm the wait function and terminals in the installed LabVIEW version.'
 ]),
 ('Run and release the notifier',[
 'Run the VI and press all_loops. Confirm that both workers stop.',
 'Notice that the graph loop may finish its current batch first. A 10 ms notifier timeout does not make the batch interruptible.',
 'Place Release Notifier after all loops have finished. Enforce this order with data dependencies or a sequence structure.',
 'Make sure the error path also terminates all loops, including the UI loop. Save and run again.'
 ])],
 note='The reference figure demonstrates shared Stop. A timing-control event or Property Node is an optional extension, not a block shown in this diagram. A notifier wait timeout is not a precise loop period.'),
 dict(title='myRIO quick tutorial 1', topic='Generate and acquire an analog signal', image='MR_01_loopback.jpg',
 goal='Build analog loopback with parallel Timed Loops and view a time trace and power spectrum.',
 caption='The diagram uses C/AO0, C/AI0, two Timed Loops and Power Spectrum PtByPt.vi.',
 groups=[
 ('Create the target VI',[
 'Open a LabVIEW myRIO project and connect to the configured station target.',
 'Create a VI under the myRIO target, not My Computer. Save it as QT4_myRIO_Loopback.vi.',
 'Open the Controls and Functions palettes. Use Search to locate the blocks shown in the figure.'
 ]),
 ('Connect analog loopback',[
 'Keep the analog output disabled while wiring. Use the connector C breakout and the myRIO pinout.',
 'Connect C/AO0 to C/AI0+. Connect C/AI0- to the specified AGND reference.',
 'Confirm the wiring and selected channels with the instructor or station guide before enabling output. Do not infer pin numbers from the block diagram.'
 ]),
 ('Build the output loop',[
 'Reproduce the Initialize, Acquire and Close organization in the reference figure. Place two parallel Timed Loops in Acquire.',
 'For each Timed Loop, select the 1 kHz timing source and request 10 ticks per iteration: nominally 10 ms.',
 'In the output loop, multiply iteration i by 0.01 to obtain time t in seconds.',
 'Use Multiply and Sine blocks to calculate sin(2 x pi x f x t). Start with f = 2 Hz and a 1 V peak sine at zero offset.',
 'Search for Analog Output and configure one-sample output on C/AO0. Wire the sine value to it and to a waveform chart.'
 ]),
 ('Build acquisition and spectrum display',[
 'In the input loop, place Analog Input and configure one-sample input on C/AI0. Wire its output to a waveform chart.',
 'Search for Power Spectrum PtByPt.vi. Wire the input samples to it. Follow the figure with a 128-sample analysis length and nominal sample rate 100 Hz; confirm terminal names in Context Help.',
 'Use Array Subset to display the first 64 spectrum elements on a Waveform Graph, as shown.',
 'Set the graph frequency scale for the configured rate and length. At 100 samples/s and 128 points, the bin spacing is 0.78125 Hz.'
 ]),
 ('Run, adjust and stop',[
 'Run at 2 Hz, then change to 5 Hz. Observe the input waveform and a spectrum feature near the selected frequency.',
 'Allow at least the initial 128-sample window to fill: nominally 1.28 s. Check actual loop timing and late iterations.',
 'Stop both loops using their Stop controls. Write AO0 = 0 V after the output loop finishes.',
 'Reset or close myRIO resources only after both loops have ended. Include output-off handling on the error path, then save the VI and project.'
 ])],
 note='These settings follow connector C. Do not apply the bipolar sine unchanged to MXP A/B outputs. Requested timing is not a hardware timing guarantee; the two loops are not synchronized sample pairs. This is direct loopback, without the RC circuit.')
]

NAVY=colors.HexColor('#16324B')
TEAL=colors.HexColor('#087F8C')
INK=colors.HexColor('#253443')
STYLE={
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=20,leading=24,textColor=NAVY,spaceAfter=4),
 'topic':ParagraphStyle('topic',fontName='Helvetica',fontSize=12,leading=16,textColor=TEAL,spaceAfter=10),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10.2,leading=14,spaceAfter=5,textColor=INK),
 'step':ParagraphStyle('step',fontName='Helvetica',fontSize=10.2,leading=14,leftIndent=18,firstLineIndent=0,spaceAfter=5,textColor=INK),
 'head':ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=11.2,leading=15,spaceBefore=9,spaceAfter=5,textColor=TEAL,keepWithNext=True),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8.3,leading=11,spaceAfter=7,textColor=INK),
}

def P(text,style='body'):
 return Paragraph(escape(text),STYLE[style])

def group(n,title,steps):
 return [P(f'{n}. {title}','head')]+[P(f'{n}.{i}  {text}','step') for i,text in enumerate(steps,1)]

def header(c,doc):
 w,h=A4
 c.setFillColor(NAVY);c.rect(0,h-10,w,10,fill=1,stroke=0)
 c.setFont('Helvetica-Bold',8);c.setFillColor(TEAL)
 c.drawString(42,h-30,'AUTOMATED TEST WORKSHOP / DAY 1')
 c.setStrokeColor(colors.HexColor('#CED8E0'));c.line(42,34,w-42,34)
 c.setFont('Helvetica',8);c.setFillColor(INK)
 c.drawString(42,22,'Practical guide | LabVIEW and myRIO')
 c.drawRightString(w-42,22,str(doc.page))

def write_markdown():
 lines=['# Day 1 - Quick tutorials','','Practical guide. Follow each section in order. Use the original figures as block-diagram references.','']
 for i,t in enumerate(CONTENT,1):
  lines += [f'## {t["title"]}', '',f'**{t["topic"]}**','',f'**Goal:** {t["goal"]}', '',f'![Figure {i}: {t["title"]}](../figs/{t["image"]})','',f'Figure {i}. {t["caption"]}','']
  for n,(title,steps) in enumerate(t['groups'],1):
   lines += [f'{n}. **{title}**']+[f'   {j}. {step}' for j,step in enumerate(steps,1)]+['']
  lines += ['**Note:** '+t['note'],'']
 lines += ['## References','','- Original tutorial figures: `LV_01_recap.md` and `myRIO_01_overview.md` in the Day 1 training materials.','- [NI myRIO-1900 user guide and pinouts](https://download.ni.com/support/manuals/376047c.pdf)','','Use Context Help for block terminals and the installed version of each function.']
 SOURCE.parent.mkdir(parents=True,exist_ok=True)
 SOURCE.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def build():
 write_markdown();OUT.parent.mkdir(parents=True,exist_ok=True)
 doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=46,bottomMargin=48,title='Day 1 - Quick tutorials: practical guide',author='Automated Test Workshop')
 flow=[]
 for i,t in enumerate(CONTENT,1):
  if i>1:flow.append(PageBreak())
  flow += [P(t['title'],'title'),P(t['topic'],'topic'),P('Goal: '+t['goal'])]
  path=FIGS/t['image']
  with PILImage.open(path) as im: iw,ih=im.size
  width=A4[0]-84; height=width*ih/iw
  flow += [Spacer(1,5),Image(str(path),width=width,height=height),P(f'Figure {i}. '+t['caption'],'small')]
  for n,(title,steps) in enumerate(t['groups'][:2],1):flow+=group(n,title,steps)
  flow += [PageBreak(),P(t['title']+' (continued)','title'),P(t['topic'],'topic')]
  for n,(title,steps) in enumerate(t['groups'][2:],3):flow+=group(n,title,steps)
  flow += [Spacer(1,8),P('Note: '+t['note'],'small')]
  if i==4:
   flow += [P('Reference: NI myRIO-1900 user guide and pinouts.','small'),Paragraph('<link href="https://download.ni.com/support/manuals/376047c.pdf" color="#087F8C">download.ni.com/support/manuals/376047c.pdf</link>',STYLE['small'])]
 doc.build(flow,onFirstPage=header,onLaterPages=header)
 print(OUT);print(SOURCE)

if __name__=='__main__':build()

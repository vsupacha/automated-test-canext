"""Build the A4 portrait Day 2 top-down practical guide (no hardware access)."""
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak,Table,TableStyle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/Day_02_Top_Down_Practical_Guide.pdf'
SOURCE=ROOT/'training_materials/worksheets/Day_02_Top_Down_Practical_Guide.md'
FIGS=ROOT/'training_materials/figs'
CONTENT=[
 dict(title='CompactDAQ tutorial 1',topic='Control switch S7 with NI-9477',image='Instr_02_Demo_Switch.jpg',
 goal='Build a complete digital-output VI, preserve the demo, then extract initialization, control and cleanup.',
 demo='demo_Switch.vi',caller='Switch_SubVI_Test.vi',
 caption='The dashed regions identify channel creation, digital write, and task stop/clear.',
 build=[
 ('Create the complete demo',[
 'Create a blank VI on My Computer. Add a physical-line control, a Boolean data control, error in and error out.',
 'Search for DAQmx Create Virtual Channel. Select Digital Output and choose the station line wired to S7; confirm the actual module name in NI MAX.',
 'Add DAQmx Write. Select Digital Bool 1Line 1Point and wire the Boolean control to data.',
 'Add DAQmx Stop Task and DAQmx Clear Task after Write, as shown. Wire task and error terminals from left to right.',
 'Use on-demand output with auto start enabled for this one-point write. Do not add sample-clock timing.'
 ]),
 ('Operate and preserve the demo',[
 'With DUT and AUX supplies off, confirm the relay wiring and active polarity. Start with the Boolean value corresponding to S7 OFF.',
 'Run once to select S7 ON, check the relay state, then run with S7 OFF. A cleared task does not by itself establish the relay state.',
 'Add an explicit OFF write before final task cleanup where the demo must finish with S7 OFF. Keep the controllable write and shutdown write distinct.',
 'Save the working VI as demos/demo_Switch.vi. Keep this complete block diagram as the later troubleshooting reference.'
 ])],
 split=[
 ('Extract the three regions',[
 'Save a copy as callers/Switch_SubVI_Test.vi. Make the following edits in this copy, leaving the demo unchanged.',
 'Select channel creation and choose Edit > Create SubVI. Save it as subvis/switch_init.vi; expose the physical line, task out and error terminals.',
 'Select only the controllable digital Write. Save it as switch_ctrl.vi; expose task in/out and the Boolean state.',
 'Select Stop Task and Clear Task together. Save them as daqmx_stop.vi. This shared cleanup releases a task; it does not switch an output off.',
 'Keep the explicit S7 OFF call in the caller before daqmx_stop. Keep physical channel configuration in switch_init.'
 ]),
 ('Reconnect and reuse',[
 'Wire switch_init -> switch_ctrl -> switch_ctrl(OFF) -> daqmx_stop with the same task reference.',
 'Run the caller with the same line and state as the demo. Compare relay action and shutdown state.',
 'For repeated changes, put switch_ctrl in the operating loop; initialize once before the loop and release the task once afterward.',
 'Save the caller and all SubVIs. Never use Run Continuously to repeatedly open hardware resources.'
 ])],
 interfaces=[('switch_init','physical line','DAQmx task'),('switch_ctrl','task, Boolean state','same task'),('daqmx_stop','task','cleanup status')],
 note='Use the verified station polarity for OFF. Call cleanup for each task that was successfully created, including the error path.'),
 dict(title='CompactDAQ tutorial 2',topic='Set the DUT supply with NI-9269',image='Instr_02_Demo_AO.jpg',
 goal='Create a two-channel DC output demo, then separate channel setup from voltage updates.',
 demo='demo_AO.vi',caller='AO_SubVI_Test.vi',
 caption='Left: create one task with two AO channels. Middle: write a two-element voltage array. Right: stop and clear.',
 build=[
 ('Create the complete demo',[
 'Create a blank VI. Add controls for the two physical AO channels and a 1D DBL array containing two voltage values.',
 'Place DAQmx Create Task, then two DAQmx Create Virtual Channel functions set to AO Voltage. Add both channels to the same task.',
 'Use the station NI-9269 ao0 and ao1 channels. Match the illustrated 0 to 10 V range only after checking the actual station wiring.',
 'Add DAQmx Write configured as Analog 1D DBL NChan 1Samp. Enable auto start for this on-demand write.',
 'Wire the array in channel-creation order: element 0 for ao0 and element 1 for ao1. Add Stop Task and Clear Task, then wire task/error flow.'
 ]),
 ('Operate and preserve the demo',[
 'Begin with [0, 0] V. Check each output with the fixture disconnected or with the approved station setup.',
 'Set the approved test voltages and run. For the illustrated fixture, [5, 5] V produces the two DUT rails through its wiring; do not assume ao1 must be -5 V.',
 'Add a final [0, 0] V write before stopping/clearing the task. Confirm both outputs return to zero.',
 'Save the complete working VI as demos/demo_AO.vi. Preserve the channel order and output-off code.'
 ])],
 split=[
 ('Extract setup and update',[
 'Save a copy as callers/AO_SubVI_Test.vi before selecting any code.',
 'Select Create Task and both Create Virtual Channel blocks. Use Edit > Create SubVI and save subvis/ao_init.vi.',
 'Expose the physical channels and configuration needed by the caller. Return the single task reference.',
 'Select the voltage Write only and create ao_update.vi. Expose task in/out and the two-element voltage array.',
 'Replace Stop/Clear with the shared daqmx_stop.vi. Do not close the task inside ao_update.'
 ]),
 ('Reconnect and reuse',[
 'Wire ao_init -> ao_update(test values) -> ao_update([0, 0]) -> daqmx_stop.',
 'Run with the same channel order and values as demo_AO.vi. Compare measured outputs, including final zero.',
 'If adding a UI loop, initialize outside it and call only ao_update when a value changes.',
 'Keep output-off handling on Stop and error paths. Save the refactored caller without replacing the original demo.'
 ])],
 interfaces=[('ao_init','AO channels, ranges','DAQmx task'),('ao_update','task, voltage array [V]','same task'),('daqmx_stop','task','cleanup status')],
 note='The screenshot supplies positive channel values; rail polarity comes from the fixture. Stopping or clearing a task is not an output-zero command.'),
 dict(title='CompactDAQ tutorial 3',topic='Read voltage with NI-9239',image='Instr_02_Demo_AI.jpg',
 goal='Acquire a finite voltage block, calculate its mean, then extract setup and measurement SubVIs.',
 demo='demo_AI.vi',caller='AI_SubVI_Test.vi',
 caption='Left: channel/timing configuration. Middle: start/read. Upper right: extract samples and calculate a mean.',
 build=[
 ('Create the complete demo',[
 'Create a blank VI with physical-channel, requested-rate, sample-count and timeout controls. Add voltage and error indicators.',
 'Place Create Task, Create Virtual Channel (AI Voltage), and DAQmx Timing (Sample Clock). Select the station NI-9239 input and approved voltage range.',
 'Select Finite Samples and begin with 10 samples as illustrated. Use a station-supported rate; the screenshot 1000 Hz is not a guaranteed NI-9239 rate.',
 'Place Start Task and DAQmx Read set to Analog Wfm 1Chan NSamp. Wire the sample count and a suitable timeout.',
 'Extract the waveform Y array and calculate its mean. Use Mean.vi or sum divided by Array Size instead of a fixed divisor when the count is configurable.',
 'Add Stop Task and Clear Task after acquisition. Wire task and error data through the full chain.'
 ]),
 ('Operate and preserve the demo',[
 'Connect an approved known DC source within the input range. Run and compare the mean with the source or reference meter.',
 'Inspect the actual DAQmx sample rate and returned sample count. The NI-9239 internal-timebase minimum is about 1.613 kS/s; the driver may coerce a requested rate.',
 'Check that the displayed number is in volts. Keep fixture scaling outside this raw-voltage demo.',
 'Save the complete working VI as demos/demo_AI.vi, including configuration, acquisition, averaging and task cleanup.'
 ])],
 split=[
 ('Extract setup and measurement',[
 'Save a copy as callers/AI_SubVI_Test.vi. Select task/channel creation and finite timing configuration; create subvis/ai_init.vi.',
 'Expose channel, requested rate and sample count. Return task out and the actual rate if required.',
 'Select Start Task, Read, sample extraction and mean calculation; create ai_measure.vi.',
 'For repeated finite acquisitions, include Stop Task after each read inside ai_measure. Keep Clear Task in the final daqmx_stop call.',
 'Expose task in/out, sample count and timeout inputs, plus mean voltage output. Return read errors; do not substitute zero for a failed measurement.'
 ]),
 ('Reconnect and reuse',[
 'Wire ai_init -> ai_measure -> daqmx_stop. Keep the same channel and acquisition settings as the saved demo.',
 'Compare mean voltage and error behavior with demo_AI.vi. Try a second known source value.',
 'Call ai_measure again using the same configured task to check the finite Start/Read/Stop lifecycle.',
 'Save the caller. Keep raw TP1 voltage and any later input-referred VOS conversion as separately named values.'
 ])],
 interfaces=[('ai_init','channel, rate, count','task, actual rate'),('ai_measure','task, count, timeout','task, mean voltage [V]'),('daqmx_stop','task','cleanup status')],
 note='Do not treat TP1 voltage as VOS directly. Confirm fixture gain, sign and settling before applying a conversion.'),
 dict(title='VISA tutorial 1',topic='Control the UDP3305S power supply',image='Instr_03_UDP3305S_Demo.jpg',
 goal='Build a complete VISA command sequence, then split connection, output control and close operations.',
 demo='demo_PPS.vi',caller='PPS_SubVI_Test.vi',
 caption='Left: VISA Open. Middle: format voltage/output-state commands and write them. Right: VISA Close.',
 build=[
 ('Create the complete demo',[
 'Find the supply in NI MAX and copy its VISA resource name. Confirm its identity with *IDN? before applying power.',
 'Create a blank VI with resource, CH1/CH2 voltage, output-enable and timeout controls. Add error in/out.',
 'Place VISA Open and set a station-appropriate timeout. Search for Format Into String and VISA Write.',
 'Reproduce the voltage and output-state command sequence in the figure. Match commands to the installed instrument programming manual.',
 'Set string constants to backslash Codes Display when writing a newline terminator. Use Format Into String for voltage and enable values.',
 'Add VISA Close after the command sequence and wire the VISA reference and error chain.'
 ]),
 ('Operate and preserve the demo',[
 'Start with both channels disabled and the approved station current limits. Check channel selection, mode, wiring and command units.',
 'Set the approved CH1/CH2 voltages. Enable the intended channels and compare the physical output with the requested settings.',
 'Add explicit output-OFF commands for both channels before VISA Close. Closing a session alone does not disable the supply.',
 'Save the complete working VI as demos/demo_PPS.vi. Preserve it as the direct SCPI troubleshooting example.'
 ])],
 split=[
 ('Extract connection and control',[
 'Save a copy as callers/PPS_SubVI_Test.vi before changing the working diagram.',
 'Select VISA Open and connection/timeout configuration. Create subvis/pps_connect.vi with resource/timeout inputs and VISA session output.',
 'Select the command-formatting and VISA Write blocks. Create pps_ctrl.vi with session in/out, two voltage values and output-enable inputs.',
 'Select VISA Close and create visa_close.vi. Use the same session type so this close SubVI can also serve the DMM.',
 'Keep output OFF as an explicit pps_ctrl call before visa_close. Do not open or close the session inside pps_ctrl.'
 ]),
 ('Reconnect and reuse',[
 'Wire pps_connect -> pps_ctrl(test settings) -> pps_ctrl(outputs OFF) -> visa_close.',
 'Use the same resource and settings as demo_PPS.vi. Compare voltage, enable behavior and shutdown.',
 'For interactive updates, keep the session open across the operating loop. Run output-OFF and close after the loop.',
 'Check the error path also attempts output OFF and closes an opened session, while retaining the original error. Save the caller and SubVIs.'
 ])],
 interfaces=[('pps_connect','resource, timeout','VISA session'),('pps_ctrl','session, voltages [V], enables','same session'),('visa_close','session','cleanup status')],
 note='AUX +/-15 V is produced by the approved dual-channel wiring, not by sending a negative setpoint blindly. Use the instrument manual for exact command syntax.'),
 dict(title='VISA tutorial 2',topic='Read DC current with UT8805E',image='Instr_03_UT8805E_Demo.jpg',
 goal='Build an open/configure/query/parse/close VI, then retain the session between measurement calls.',
 demo='demo_DMM.vi',caller='DMM_SubVI_Test.vi',
 caption='Left: open/configure DC current. Middle: READ? and VISA Read. Right: string-to-number conversion and close.',
 build=[
 ('Create the complete demo',[
 'Find the DMM in NI MAX and verify *IDN?. Create a blank VI with resource, timeout, current-range and current/error indicators.',
 'Place VISA Open. Reproduce the illustrated DC current configuration, range selection and one-sample command sequence using VISA Write.',
 'Use the station-approved range, with 20 mA as the illustrated current range. Confirm syntax and terminators against the actual DMM manual.',
 'Write READ?, then call VISA Read. Use the instrument response termination and enough buffer space for the complete response; the illustrated byte count is only an example.',
 'Convert the numeric reply using a suitable string-to-number function. Display the value in A, or explicitly multiply by 1000 and label mA.',
 'Place VISA Close after conversion. Wire the VISA reference and error flow through every communication step.'
 ]),
 ('Operate and preserve the demo',[
 'With circuit power off, confirm the DMM current terminals and fuse/range. Insert the current path in series through the approved fixture.',
 'Apply the approved current source or powered fixture, run the VI and compare the display with the instrument front panel.',
 'Check that a communication/parse failure is reported as an error rather than a valid 0 A result. De-energize the fixture before changing wiring.',
 'Save the complete working VI as demos/demo_DMM.vi, including initialization, query, parsing and close.'
 ])],
 split=[
 ('Extract connection and reading',[
 'Save a copy as callers/DMM_SubVI_Test.vi.',
 'Select VISA Open and the DC-current/range/sample-count configuration. Create subvis/dmm_connect.vi.',
 'Expose resource, range and timeout settings as needed, with VISA session out and error out.',
 'Select READ?, VISA Read and numeric conversion only. Create dmm_read.vi with session in/out and current in A.',
 'Keep VISA Close outside dmm_read and replace it with shared visa_close.vi. The session must remain valid for another reading.'
 ]),
 ('Reconnect and reuse',[
 'Wire dmm_connect -> dmm_read -> visa_close using the same session reference.',
 'Compare the returned current with demo_DMM.vi at the same range and source condition.',
 'Call dmm_read more than once before closing to confirm session reuse. Use the same timeout and numeric units.',
 'When the demo is part of a powered fixture, disable stimulus before closing resources. Save the caller and SubVIs.'
 ])],
 interfaces=[('dmm_connect','resource, range, timeout','VISA session'),('dmm_read','session','session, current [A]'),('visa_close','session','cleanup status')],
 note='Do not place a current-mode DMM directly across a supply. Compare engineering units as well as numerical values during refactoring.')
]
NAVY=colors.HexColor('#16324B');TEAL=colors.HexColor('#087F8C');INK=colors.HexColor('#253443')
S={
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=19,leading=23,spaceAfter=5,textColor=NAVY),
 'topic':ParagraphStyle('topic',fontName='Helvetica',fontSize=12,leading=16,spaceAfter=9,textColor=TEAL),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=13.5,spaceAfter=5,textColor=INK),
 'step':ParagraphStyle('step',fontName='Helvetica',fontSize=10,leading=13.5,leftIndent=16,spaceAfter=5,textColor=INK),
 'head':ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=11,leading=14,spaceBefore=8,spaceAfter=5,textColor=TEAL,keepWithNext=True),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8.2,leading=10.5,spaceAfter=6,textColor=INK)}
def P(t,style='body'):return Paragraph(escape(t),S[style])
def group(n,title,steps):return [P(f'{n}. {title}','head')]+[P(f'{n}.{j}  {s}','step') for j,s in enumerate(steps,1)]
def header(c,d):
 w,h=A4;c.setFillColor(NAVY);c.rect(0,h-10,w,10,fill=1,stroke=0)
 c.setFont('Helvetica-Bold',8);c.setFillColor(TEAL);c.drawString(42,h-30,'AUTOMATED TEST WORKSHOP / DAY 2')
 c.setStrokeColor(colors.HexColor('#CED8E0'));c.line(42,34,w-42,34)
 c.setFont('Helvetica',8);c.setFillColor(INK);c.drawString(42,22,'Practical guide | Working demo first, reusable SubVIs next');c.drawRightString(w-42,22,str(d.page))
def interface_table(rows):
 data=[[P(x,'small') for x in row] for row in [('SubVI','Inputs','Outputs')]+rows]
 t=Table(data,colWidths=[110,205,196],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF1F5')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),0.4,colors.HexColor('#CED8E0')),('INNERGRID',(0,0),(-1,-1),0.3,colors.HexColor('#CED8E0')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
 return t
INTRO=[
 ('Start with a complete operation',[
 'Define the task as Configure -> Operate or Measure -> Return to safe state -> Release resources.',
 'Create the complete low-level diagram in one VI. Use the reference figure to identify the required blocks.',
 'Use physical-channel/resource controls and visible outputs so each device can be checked independently.'
 ]),
 ('Preserve a working demo before refactoring',[
 'Test normal operation and shutdown on the configured station.',
 'Save the full working diagram in a demos folder. Keep the filenames used in the following tutorials.',
 'Create a separate caller copy for refactoring. Do not overwrite the full demo with a diagram made only of SubVI calls.'
 ]),
 ('Extract one responsibility at a time',[
 'Select a functional region, then use Edit > Create SubVI. Save it in a subvis folder.',
 'Give each SubVI a clear icon and connector pane: settings/reference/error inputs on the left, measurements/reference/error outputs on the right.',
 'Keep setup and final cleanup outside repeated read/write calls. Use the same task or VISA session throughout its lifetime.',
 'Run after each extraction and compare with the saved demo before extracting the next region.'
 ]),
 ('Keep demos and reusable code together',[
 'Use one LabVIEW project with demos/, subvis/ and callers/ folders. Save all dependencies before closing the project.',
 'Create driver code on My Computer. Open the Controls/Functions palettes, use Search to locate blocks, and Ctrl+H for terminal help.',
 'The following pages describe VIs to build in LabVIEW; this guide does not provide executable demo VIs.'
 ])]
FINAL=[
 ('Prepare one coordination VI',[
 'Create callers/LM321_Measurement_Demo.vi. Select the station channels and VISA resources through Front Panel controls.',
 'Call pps_connect, dmm_connect, switch_init, ao_init and ai_init once. Retain the five references in the caller.',
 'Before applying power, check the DIB connections and relay states against the Day 2 fixture diagram.'
 ]),
 ('Use the SubVIs in the measurement order',[
 'Use pps_ctrl for the approved AUX supply settings and ao_update for the DUT supply settings. Sequence related operations using error/data dependencies.',
 'Select the measurement path with switch_ctrl and allow the fixture to settle before reading.',
 'Use ai_measure for TP1 voltage and dmm_read for current under their respective approved fixture configurations.',
 'Keep TP1 volts, derived VOS volts and current amperes separately named. Apply only the station-verified fixture gain and sign; the reference divider is approximately 1000:1.',
 'Compare with the original single-device demos before adding limits or automated pass/fail decisions.'
 ]),
 ('Shut down explicitly',[
 'Disable DUT and AUX outputs and return relays to the station-defined state before releasing references.',
 'Call daqmx_stop for every created DAQmx task and visa_close for each opened VISA session.',
 'Attempt cleanup even when an earlier operation fails: preserve the first error, execute the needed cleanup actions for valid references, then combine/report cleanup errors.',
 'Do not wire a stale incoming error blindly through output-off code that skips execution on error. Review this behavior in each cleanup path.',
 'Save the coordination VI and dependencies. Keep all five original demos available for later troubleshooting and Day 3 integration.'
 ])]
REFS=[('Create and configure a LabVIEW SubVI','https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000YK4VCAW'),('NI-DAQmx task lifecycle','https://www.ni.com/en/support/documentation/supplemental/06/learn-10-functions-in-ni-daqmx-and-handle-80-percent-of-your-dat.html'),('NI-9239 supported data rates','https://download.ni.com/support/manuals/375939b_02.pdf')]
def write_md():
 a=['# Day 2 - Top-down instrument programming','','Build a working demo first, preserve it, then extract reusable SubVIs.','']
 for n,title,steps in [(i,t,s) for i,(t,s) in enumerate(INTRO,1)]:a += [f'{n}. **{title}**']+[f'   {j}. {s}' for j,s in enumerate(steps,1)]+['']
 for i,t in enumerate(CONTENT,1):
  a += [f'## {t["title"]}: {t["topic"]}','',f'**Goal:** {t["goal"]}','',f'![Figure {i}](../figs/{t["image"]})','',f'Figure {i}. {t["caption"]}','']
  for n,(title,steps) in enumerate(t['build']+t['split'],1):a += [f'{n}. **{title}**']+[f'   {j}. {s}' for j,s in enumerate(steps,1)]+['']
  a += ['### SubVI interfaces','','All SubVIs also have error in/error out. Update/control/read VIs pass through the same reference.','','| SubVI | Inputs | Outputs |','| --- | --- | --- |']+['| '+' | '.join(row)+' |' for row in t['interfaces']]+['','**Note:** '+t['note'],'']
 a+=['## Coordinate the instruments','']
 for n,(title,steps) in enumerate(FINAL,1):a += [f'{n}. **{title}**']+[f'   {j}. {s}' for j,s in enumerate(steps,1)]+['']
 a+=['## References','','Original block figures: Instr_02_cDAQ.md and Instr_03_VISA.md. Figures are unchanged; added shutdown and configurable-count instructions extend the pictured demos.','']+[f'- [{title}]({url})' for title,url in REFS]
 SOURCE.parent.mkdir(parents=True,exist_ok=True);SOURCE.write_text('\n'.join(a)+'\n',encoding='utf-8')
def build():
 write_md();OUT.parent.mkdir(parents=True,exist_ok=True)
 f=[P('Day 2 practical guide','title'),P('Top-down instrument programming','topic'),P('Goal: build complete device demos, preserve them, then extract reusable SubVIs.')]
 for n,(title,steps) in enumerate(INTRO,1):f+=group(n,title,steps)
 f += [P('Working order: complete demo -> saved reference -> refactored caller -> verified SubVIs.','head'),P('No results forms or submission tasks are required. Work with the station configuration; no hardware validation is claimed by this guide.','small')]
 for i,t in enumerate(CONTENT,1):
  f += [PageBreak(),P(t['title'],'title'),P(t['topic'],'topic'),P('Goal: '+t['goal'])]
  p=FIGS/t['image']
  with PILImage.open(p) as im:iw,ih=im.size
  width=A4[0]-84;f += [Spacer(1,4),Image(str(p),width=width,height=width*ih/iw),P(f'Figure {i}. '+t['caption'],'small')]
  for n,(title,steps) in enumerate(t['build'],1):f+=group(n,title,steps)
  f += [PageBreak(),P(t['title']+' (continued)','title'),P('Refactor the saved demo','topic')]
  for n,(title,steps) in enumerate(t['split'],3):f+=group(n,title,steps)
  f += [P('SubVI interfaces','head'),P('Every SubVI also has error in/error out. Pass the same reference through control/read calls.','small'),interface_table(t['interfaces']),Spacer(1,8),P('Note: '+t['note'],'small')]
 f += [PageBreak(),P('Coordinate the instruments','title'),P('Reuse the SubVIs for the LM321 fixture','topic')]
 for n,(title,steps) in enumerate(FINAL,1):f+=group(n,title,steps)
 f += [P('References','head'),P('Original figures: Instr_02_cDAQ.md and Instr_03_VISA.md. Shutdown and configurable-count instructions extend the illustrated demos.','small')]
 for title,url in REFS:f.append(Paragraph(f'<link href="{escape(url)}" color="#087F8C">{escape(title)}</link>',S['small']))
 d=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=46,bottomMargin=48,title='Day 2 - Top-down instrument programming',author='Automated Test Workshop')
 d.build(f,onFirstPage=header,onLaterPages=header);print(OUT);print(SOURCE)
if __name__=='__main__':build()

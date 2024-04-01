# Aneng AN9002 Bluetooth DMM data logger (fork) + big mechanical/electrical design flaw!

This is more or less a fork from https://github.com/riktw/AN9002_info. @riktw, thanks a lot!

Since I'm also reporting about the flaw, I decided to start a new repository.

## About the logger:
- I introduced a log file 'an9002.csv' with the format: Table of timestamp and value. Easy to use in spreadsheet programs to show a graph and delete misreadings.
- Use the ESC button to stop logging.

### IMPORTANT:
- Make shure, you start the DMM in continuous mode! The script doesn't save the 'an9002.csv' when DMM shuts down in auto power off mode (from the manual: To disable the Auto Power Off function, hold down the SEL button when turning on the product, you will hear five beeps if you have successfully disabled the function).
- Works just with adminitrator rights! (https://github.com/riktw/AN9002_info/issues/1#issuecomment-1155512464)

More information can be found in 'an9002_data_logger.py' and of course (https://github.com/riktw/AN9002_info).

## About the mechanical/electrical problem:

After about 100 mating cycles of any input terminal, connection is completly gone!

![an9002_pcb](https://github.com/hcet14/Aneng-AN9002-Bluetooth-DMM-data-logger-fork-big-mechanical-electrical-design-flaw-/assets/38034498/ad713de6-7d9f-48ed-bdef-b3a1858c99ef)
![an9002_terminals_marked](https://github.com/hcet14/Aneng-AN9002-Bluetooth-DMM-data-logger-fork-big-mechanical-electrical-design-flaw-/assets/38034498/8af061d0-7322-446b-9735-eb96fc9b6010)

The vertical opening is the killer, causing the terminals to wear out!

![an9002_terminal_fix](https://github.com/hcet14/Aneng-AN9002-Bluetooth-DMM-data-logger-fork-big-mechanical-electrical-design-flaw-/assets/38034498/e01e5c16-622f-494e-bce3-0ecddbca4846)

I don't recommend doing this like I did. The two wires where way to thick. Maybe 4 wires with a thinner diameter might work.

Second best solution, close the gap with solder.


![female_banana socket_4mm_git2](https://github.com/hcet14/Aneng-AN9002-Bluetooth-DMM-data-logger-fork-big-mechanical-electrical-design-flaw-/assets/38034498/b12ed6e7-1440-4e16-a134-01ae3790fcdc)

Best solution, replace the terminals with something like above. 

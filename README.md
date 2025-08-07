# JBC_T245_soldering_station
This repository shows a controller for the JBC T245 handle. In contrast to other designs, this design is powered by DC and has an earthed tip nonetheless.

# Whats the motivation behind this project?
I was tired of my ERSA RDS80 soldering station - the standard hollow tips on a heating element just don't provide the thermal performance needed for PCBs with wide groudplanes or big connectors. The cheap cartridge-based stations with the T12 tips are also an alternative, but the cheap tips did not really impress me regarding durability. Thats why I decited to build a station with the phenomenal and durable JBC tips and the high quality handpiece that has similar performance to the original.

# Whats special with this project?
Several T245 controller projects either are rather complex or are using AC transformers. However, the transformers necessary are heavy and take up alot of space inside the housing. This station uses a standard 24V 350W SELV power supply as its used by many 3D printers. Okay, I get it - a transformer is definetely not bigger than the clunky power supply. However, I use the power supply for powering the rest of my home lab, too (like my homemade PSU for example). So thats why this is a little bit more space-saving, at least for me. Another advantage in my opinion is that the controller does not need any 230V wiring inside, making it somewhat safer as a DIY project.

# What may be missing?
The controller does not implement any kind of standby-feature. This may be done in software, but I did not have the chance to implement it just now.

# Additional info:
The cartridge pinout is taken from the reverse-engineered schematic of the JBC CD-2BC station (thanks to johnmx!):
[Link](https://www.eevblog.com/forum/testgear/jbc-soldering-station-cd-2bc-complete-schematic-analysis/)



## DISCLAIMER:

This project involves working with electricity, which can be dangerous and potentially fatal if not handled properly. It is intended for individuals with sufficient knowledge of electronics and electrical safety.

By using, modifying, or building this project, you acknowledge and agree that:

You do so at your own risk.

The authors and contributors of this project assume no responsibility or liability for any damage, injury, or legal consequences resulting from the use or misuse of this hardware, software, or any related documentation.

Electrical standards and regulations vary by country or region. It is your responsibility to ensure that your implementation complies with local laws, regulations, and safety codes.

This project is provided "as is", without any express or implied warranties, including but not limited to fitness for a particular purpose.

If you are unsure about any aspect of electrical safety or regulatory compliance, do not attempt to build or operate this project without consulting a qualified professional.

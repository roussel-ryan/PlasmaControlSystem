# PlasmaControlSystem
ControlSystem is the application for interfacing with the AWA plasma source, mainly using TKinter

5_25_2017 - Project Start



Process control flow
---------------------------------------------------
Considerations: We need to constantly update the the displayed values measured from our devices which takes time, leading to GUI unresponsiveness. In order to handle this we use two threads, a worker to send queries/commands the hardware and one to render the GUI and populate the queue with tasks.

We use a queue system to communicate between the two threads. The GUI adds tasks to the queue such as "set the current of the solenoid to 5A", while the internal model adds periodic queries and status updates to the queue and the worker processes the commands in the order recieved. The worker can write to an internal model of the system and the GUI displays the data stored in the internal model.

In order for this to work the internal model must have objects represnatative of each component in the system capable of the following:
- name
- specific query method
- specific command method
- method to lock/unlock device
- physical attribute storage accessable by the GUI
- interlock state such that commands cannot be set if device is locked


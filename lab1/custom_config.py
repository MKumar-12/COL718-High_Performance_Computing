import m5
from m5.objects import *
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run gem5 simulation with different configs.")
parser.add_argument("--cpu", type=str, default="TimingSimpleCPU", help="CPU model")
parser.add_argument("--freq", type=str, default="1GHz", help="CPU frequency")
parser.add_argument("--mem", type=str, default="DDR3_1600_8x8", help="Memory model")
args = parser.parse_args()

# Create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = args.freq
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range

# Create the CPU model based on the argument
if args.cpu == "TimingSimpleCPU":
    system.cpu = TimingSimpleCPU()
elif args.cpu == "DerivO3CPU":
    system.cpu = DerivO3CPU()
elif args.cpu == "AtomicSimpleCPU":
    system.cpu = AtomicSimpleCPU()
    system.mem_mode = "atomic"
else:
    raise ValueError(f"Unknown CPU model: {args.cpu}")

# Create a memory bus, a system crossbar, in this case
system.membus = SystemXBar()

# Hook the CPU ports up to the membus
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# Create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()

# X86-specific interrupt connections
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Create a memory controller and connect it to the membus
system.mem_ctrl = MemCtrl()
if args.mem == "DDR3_1600_8x8":
    system.mem_ctrl.dram = DDR3_1600_8x8()
elif args.mem == "DDR4_2400_8x8":
    system.mem_ctrl.dram = DDR4_2400_8x8()
elif args.mem == "DDR3_2133_8x8":
    system.mem_ctrl.dram = DDR3_2133_8x8()
elif args.mem == "DDR5_4400_4x8":
    system.mem_ctrl.dram = DDR5_4400_4x8()
elif args.mem == "LPDDR5_5500_1x16_8B_BL32":
    system.mem_ctrl.dram = LPDDR5_5500_1x16_8B_BL32()
else:
    raise ValueError(f"Unknown memory model: {args.mem}")

system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

# Set the workload binary
binary = 'mm.1'
system.workload = SEWorkload.init_compatible(binary)

# Create a process for a simple "Hello World" application
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Starting simulation with {args.cpu} @ {args.freq} and {args.mem}!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
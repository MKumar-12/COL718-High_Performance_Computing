import m5
from m5.objects import *
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run gem5 simulation with different configs.")
parser.add_argument("--cpu", type=str, default="TimingSimpleCPU", help="CPU model")
parser.add_argument("--bp", type=str, default="TAGE", help="Branch Predictor Method")
args = parser.parse_args()

# Create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# Create the CPU model based on the argument
if args.cpu == "TimingSimpleCPU":
    system.cpu = TimingSimpleCPU()
elif args.cpu == "DerivO3CPU":
    system.cpu = DerivO3CPU()
else:
    raise ValueError(f"Unknown CPU model: {args.cpu}")

# Assign the branch predictor
if args.bp == "BiModeBP":
    system.cpu.branchPred = BiModeBP()
elif args.bp == "TournamentBP":
    system.cpu.branchPred = TournamentBP()
elif args.bp == "LocalBP":
    system.cpu.branchPred = LocalBP()
elif args.bp == "TAGE":
    system.cpu.branchPred = TAGE()
else:
    raise ValueError(f"Unknown branch predictor: {args.bp}")

# Create a memory bus and connect the components
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Create a memory controller and connect it to the membus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR4_2400_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

# Set the workload binary
binary = 'mm_blocked.1'
system.workload = SEWorkload.init_compatible(binary)

# Create a process for the blocked matrix multiplication binary
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Starting simulation with {args.cpu} using {args.bp} Branch Predictor!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
import m5
from m5.objects import *
import argparse
import sys

# Add path for including caches.py
sys.path.append('/mnt/c/Users/manis/OneDrive/Desktop/gem5/configs/learning_gem5/part1/')
sys.path.append('/mnt/c/Users/manis/OneDrive/Desktop/gem5/configs/') 

from caches import L1ICache, L1DCache, L2Cache

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run gem5 simulation with different configs.")
parser.add_argument("--cpu", type=str, default="TimingSimpleCPU", help="CPU model")
parser.add_argument("--size_L1i", type=str, default="16kB", help="L1 Instruction cache size")
parser.add_argument("--size_L1d", type=str, default="32kB", help="L1 Data cache size")
parser.add_argument("--size_L2", type=str, default="256kB", help="L2 cache size")

parser.add_argument("--assoc_L1", type=int, default=2, help="L1 cache associativity")
parser.add_argument("--tag_latency_L1", type=int, default=2, help="L1 cache tag latency")
parser.add_argument("--data_latency_L1", type=int, default=2, help="L1 cache data latency")
parser.add_argument("--response_latency_L1", type=int, default=2, help="L1 cache response latency")
parser.add_argument("--assoc_L2", type=int, default=8, help="L2 cache associativity")
parser.add_argument("--tag_latency_L2", type=int, default=20, help="L2 cache tag latency")
parser.add_argument("--data_latency_L2", type=int, default=20, help="L2 cache data latency")
parser.add_argument("--response_latency_L2", type=int, default=20, help="L2 cache response latency")

parser.add_argument("--bin_exec", type=str, default="mm_simple.1", help="Binary file")
args = parser.parse_args()

# Create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  

# Create the CPU model based on the argument
if args.cpu == "TimingSimpleCPU":
    system.cpu = TimingSimpleCPU()
elif args.cpu == "DerivO3CPU":
    system.cpu = DerivO3CPU()
else:
    raise ValueError(f"Unknown CPU model: {args.cpu}")

# Create a memory bus and connect the components
system.membus = SystemXBar()

# Setup L1i cache parameters
system.cpu.icache = L1ICache()                   
system.cpu.icache.size = args.size_L1i     
system.cpu.icache.assoc = args.assoc_L1
system.cpu.icache.tag_latency = args.tag_latency_L1
system.cpu.icache.data_latency = args.data_latency_L1
system.cpu.icache.response_latency = args.response_latency_L1    

# Setup L1d cache parameters
system.cpu.dcache = L1DCache()
system.cpu.dcache.size = args.size_L1d
system.cpu.dcache.assoc = args.assoc_L1
system.cpu.dcache.tag_latency = args.tag_latency_L1
system.cpu.dcache.data_latency = args.data_latency_L1
system.cpu.dcache.response_latency = args.response_latency_L1

# Connect L1 caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Setup L2 cache and crossbar(L2 bus)
system.l2bus = L2XBar()

# Setup L2 cache parameters
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache()
system.l2cache.size = args.size_L2
system.l2cache.assoc = args.assoc_L2
system.l2cache.tag_latency = args.tag_latency_L2
system.l2cache.data_latency = args.data_latency_L2
system.l2cache.response_latency = args.response_latency_L2

# Connect L2 cache to the L2 bus and memory bus
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

# Create the interrupt controller for the CPU and connect to the membus
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
binary = args.bin_exec
system.workload = SEWorkload.init_compatible(binary)

# Create a process for the matrix multiplication binary
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Starting simulation - CPU model: {args.cpu}\n"
      f"L1-iCache: {args.size_L1i}\t, Associativity: {args.assoc_L1}, "
      f"Tag Latency: {args.tag_latency_L1}, Data Latency: {args.data_latency_L1}, "
      f"Response Latency: {args.response_latency_L1}\n"
      f"L1-dCache: {args.size_L1d}\t, Associativity: {args.assoc_L1}, "
      f"Tag Latency: {args.tag_latency_L1}, Data Latency: {args.data_latency_L1}, "
      f"Response Latency: {args.response_latency_L1}\n"
      f"L2-Cache : {args.size_L2}\t, Associativity: {args.assoc_L2}, "
      f"Tag Latency: {args.tag_latency_L2}, Data Latency: {args.data_latency_L2}, "
      f"Response Latency: {args.response_latency_L2}")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
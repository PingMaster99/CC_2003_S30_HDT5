import simpy
import random
import statistics

# Algoritmos y Estructuras de Datos
# Catedratico Julio Ayala
# Auxiliares Luis Delgado y Edgar Toledo
# Pablo Ruiz 18259 (PingMaster99)


random.seed(707070)
timeValues = []
numberOfProcesses = 25    # Defines the amount of processes to be executed
CPUCores = 1              # Number of processors
CPUThreads = 3            # Number of instructions executed by each processor
RAMCapacity = 100         # RAM size
instructionInterval = 10  # Speed at which processes are received, higher is faster (cannot be zero)


def proceso(name, env, cpu, wait, RAM):
    timeReceived = env.now    # Time the instruction is received
    RAMQuantity = random.randint(1, 10)    # RAM required
    instructionNumber = random.randint(1, 10)    # Number of steps in the instruction

    print('%s arrives at %f, needs %d of RAM, and has %d instructions' %
          (name, timeReceived, RAMQuantity, instructionNumber))

    # Allocates ram to the instruction if available
    with RAM.get(RAMQuantity) as allocatedRAM:
        yield allocatedRAM
        yield env.timeout(1)
        print("%s READY" % name)    # Instruction is ready once RAM is allocated

        # Instruction is in CPU while it still has instructions left
        while instructionNumber > 0:
            print('%s RUNNING' % name)    # CPU runs the instruction
            # Instruction is assigned a turn in the CPU
            with cpu.request() as turn:
                yield turn
                # If the instruction count is less than the number of threads, the processor is released sooner
                if instructionNumber <= CPUThreads:
                    yield env.timeout(1)
                    instructionNumber = 0   # Instruction is finished
                # If the instruction has more than 3 instructions, it processes only 3 of them
                else:
                    yield env.timeout(1)
                    instructionNumber -= CPUThreads
                    # Checks to see if it needs to perform IO operations
                    if random.randint(1, 2) == 1:
                        # Performs the IO operations
                        with wait.request() as operation:
                            yield operation
                            print("%s WAITING" % name)
                            yield env.timeout(1)

        # Returns the amount of RAM allocated
        with RAM.put(RAMQuantity) as returnRAM:
            yield env.timeout(1)
            yield returnRAM

    # Records the process time
    totalTime = env.now - timeReceived
    print('%s TERMINATED in %f' % (name, totalTime))
    timeValues.append(totalTime)
    print()


# Conditions for the simulating environment
env = simpy.Environment()   # Simulation environment
RAM = simpy.Container(env, init=RAMCapacity, capacity=RAMCapacity)
CPU = simpy.Resource(env, capacity=CPUCores)
WAITING = simpy.Resource(env, capacity=1)   # Queue of I/O


# Runs the processes
def main(environment, ram, cpu, waiting):
    for i in range(numberOfProcesses):
        env.process(proceso("PROCESS %d" % i, environment, cpu, waiting, ram))
        yield env.timeout(random.expovariate(1.0 / instructionInterval))


# Runs the environment
env.process(main(env, RAM, CPU, WAITING))
env.run()

# Prints the needed statistics from the process times
print("The average process time is %f" % statistics.mean(timeValues))
print("Its standard deviation is %f" % statistics.stdev(timeValues))


import gsr
import ml

def main():

    """
    Example
    state 1 : calibration
    state 2 : focus
    state 3 : rest
    ...
    """

    sets = [int(i) for i in sys.argv[1:]]
    print(sets)
    process_gsr = gsr.measure_gsr()
    process_gsr.measure(sets)

if __name__ == '__main__':
    main()

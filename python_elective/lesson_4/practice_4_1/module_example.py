import first_module.print as fp
import second_module.print

if __name__ == '__main__':
    print(fp.printing.__doc__)
    fp.printing()
    second_module.print.printing()


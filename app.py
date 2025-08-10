import sys


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    try:
        print(sys.argv[1])
    except IndexError:
        print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

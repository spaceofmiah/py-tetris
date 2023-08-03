# py-tetris
Tetris game 



### Running application 

**On Windows**

> Pre-requisite
> Make sure to have git bash installed
> https://git-scm.com/downloads


open up git bash and navigate to project folder and run

```bash
.\tetris.sh < input.txt > output.txt
```

**On Linux**

Open your bash shell and navigate to project folder and run

```bash
.\tetris.sh < input.txt > output.txt
```

Above command would run the application with the given input and redirect the program result to a file named `output.txt`


## TESTING THE APPLICATION

```python
python sample_test.py
```


## Building `tetris.py` to `tetris.exe`

> Pre-requisite
>
> Install application builder dependencies

To build the python program to `.exe`, navigate to project directory and run 

```bash
pip install -r requirements.txt
```

The above command would install the required dependency to convert the python script to executable. Run the below command to create an executable off the python script

```bash
pyinstaller tetris.py
```

**Running the executable**

On successful build, you should have a `./dist/tetris/tetris.exe` file, this would be the full path with which to start the application. so in your command line you could run

```bash
./dist/tetris/tetris.exe input.txt
```

And that should automatically run the program with the given input file. Above command would output result on stdout, to redirect the result to a file, use


```bash
./dist/tetris/tetris.exe input.txt > output.txt
```


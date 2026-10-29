<h3>That's just a small class project, meant to test the use of scripts in the terminal and reading and the saving in python.
<br><i>Could contain lots of errors.</i></h3>
<br>
All the text and comments are in french, but the code is in English. I don't know why.
<br>
Ask a number of time a random capital and country to know about.
<br><i><b> I do not think coming back on it.</b></i>
<br> I've already implemented a lot of features and I think it's enough for a small project...
<br> These Informations are to give to the program at it's launch. <br>like : '<i><b>python capitales.py 2 1</b></i>'
<br>-
<table align=center>
    <tr>
        <td><b><h4>Variable</h4></b></td>
        <td><b><h4>Entry Data Type</h4></b></td>
        <td><b><h4>Description</h4></b></td>
        <td><b><h4>Shortcut</h4></b></td>
    </tr>
    <tr>
        <td><b>Question number</b></td>
        <td><i>int</i></td>
        <td>Describe the number of questions to ask.</td>
        <td><b>/n:</b>(<i>number</i>)</td>
    </tr>
    <tr>
        <td><b>Question mode</b></td>
        <td><i>int</i></td>
        <td>Gives a choice between 2 type of questions in 4 modes by asking for : 
        <br>-<b>1</b>:a capital; -<b>2</b>:a country, -<b>3-4</b>:both(1/2basis or random) </td>
        <td><b>/m:</b>(<i>number</i>)</td>
    </tr>
    <tr>
        <td><b>Save mode</b></td>
        <td><i>int</i></td>
        <td>Gives a choice between 3 saving modes :
        <br>-<b>1</b>:Create a new file; -<b>2-3</b>:Using an existing(<i>creating if not exists</i>){appending or wrinting} </td>
        <td><b>/s:</b>(<i>number</i>)</td>
    </tr>
    <tr>
        <td><b>Origin File</b></td>
        <td><i>string</i></td>
        <td>Is the file where the questions will come from.</td>
        <td><b>/of:</b>(<i>file's Name</i>)</td>
    </tr>
    <tr>
        <td><b>Save File</b></td>
        <td><i>string</i></td>
        <td>Is the file were chosen data will go.(<i>by the saveType</i>)</td>
        <td><b>/sf:</b>(<i>file's Name<i>)</td>
    </tr>
    <tr>
        <td><b>Specifications</b></td>
        <td><i>string</i></td>
        <td>The differents options that can be added :
        <br>-'r' : results show the resuslts of the test
        <br>-'e' : ephemeral, no questions on saving the data
        <br>-'S' : Save. Activate all  in default settings to save with no questions.</td>
        <td><b>/:</b>(<i>composition</i>)</td>
    </tr>
</table>
<br>In the system, the <b><i>unmarked</i></b> information will have less importance, <br> as the signed ones can be placed anywhere (as long there's spacing)
<br><br> Each data type is processed apart from another, <br>in example, <i><b>1 2 3</b></i> <br>equals <i><b>/s:3 /m:2 /n:1</b></i>, <br>equals <i><b>2 /n:1 3</b></i>, <br>and <i><b>1 2 3 4</b></i> it <b>throws an error</b> (too much of the same type : int).
<br> A data type does not affect another.
<br><br>I could implement the saveType but, I <b>can</b> not to.
<br>(it is also the only way left to reject the saving ? to see)
<br>There is <b>much</b> left to do but I will leave it like that. 

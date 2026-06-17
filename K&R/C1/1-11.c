/* Exercise 1-11. How would you test the word count program? What kinds of input are most
likely to uncover bugs if there are any?

- new line always have at least one, because enter counts as new line.
- character count always have "more" because new line, tabs and spaces counts as characters.
❯ ./main
		adl


			  d

nl: 5  nw: 2  nc: 18
❯ ./main
nl: 0  nw: 0  nc: 0
❯ ./main
		

nl: 2  nw: 0  nc: 4
❯ ./main
hello
nl: 1  nw: 1  nc: 6
❯ ./main
hello	world
nl: 1  nw: 2  nc: 12
❯ ./main
hello
     nl: 1  nw: 1  nc: 11
❯ ./main
hello       world
nl: 1  nw: 2  nc: 18
❯ ./main
       hello
nl: 1  nw: 1  nc: 13
❯ ./main
	hello
nl: 1  nw: 1  nc: 7
❯ ./main
hello          
nl: 1  nw: 1  nc: 16
❯ ./main
hello	world
this          is	c
nl: 2  nw: 5  nc: 31
❯ ./main
a
b
c
nl: 3  nw: 3  nc: 6
❯ ./main
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
nl: 1  nw: 1  nc: 72
❯ ./main
a  b c	d		e f   g
nl: 1  nw: 7  nc: 18
*/

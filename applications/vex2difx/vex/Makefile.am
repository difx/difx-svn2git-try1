
AM_YFLAGS = -d -y
AM_CPPFLAGS = -Dyyerror=vexerror -Dyylval=vexlval -Dyyin=vexin -Dyyparse=vexparse -Dyylex=vexlex

BUILT_SOURCES = \
	vex_parse.tab.h \
	vex_parse.c 

noinst_LTLIBRARIES = \
	libvex.la

vex_parse.tab.h: $(srcdir)/vex_parse.y
	bison -d $(srcdir)/vex_parse.y

print_vex.o: vex_parse.tab.h

libvex_la_SOURCES = \
	print_vex.c \
	vexf.c \
	vexf_put.c \
	vex_get.c \
	vex_put.c \
	vex_util.c \
	vex_parse.h \
	vex_parse.y \
	vex.h \
	vex.yy.l

CLEANFILES = vex_parse.tab.[ch] vex_parse.[ch] vex.yy.c

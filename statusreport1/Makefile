TEX = pdflatex
BIB = bibtex
TARGET = statusreport1

all : buildpdf

buildpdf :
	$(TEX) $(TARGET) && $(BIB) $(TARGET) && $(TEX) $(TARGET) && $(TEX) $(TARGET)

clean :
	rm *.aux *.bbl *.log *.blg *.out *.pdf
  

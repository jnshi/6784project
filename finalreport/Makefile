TEX = pdflatex
BIB = bibtex
TARGET = finalreport

all : buildpdf

buildpdf :
	$(TEX) $(TARGET) && $(BIB) $(TARGET) && $(TEX) $(TARGET) && $(TEX) $(TARGET)

clean :
	rm *.aux *.bbl *.log *.blg *.out *.pdf
  

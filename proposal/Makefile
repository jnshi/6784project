TEX = pdflatex
BIB = bibtex

all : proposal.pdf

proposal.pdf :
	$(TEX) proposal && $(BIB) proposal && $(TEX) proposal && $(TEX) proposal

clean :
	rm *.aux *.bbl *.log *.blg *.out *.pdf
  

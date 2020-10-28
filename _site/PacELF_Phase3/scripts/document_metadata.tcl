# Creating metadata documents for PacELF Phase 2 pdf files
# Metadata will be in .xml format

if { [ xvalue exists [asset.doc.namespace.exists :namespace "rdsi.pacelf.phase3"]] == "false" } {
  asset.doc.namespace.update :create true :namespace rdsi.pacelf.phase3 :description "PacELF documents"
}

# Document: rdsi.pacelf.phase3:document

asset.doc.type.update \
  :create "true" \
  :type rdsi.pacelf.phase3:document \
  :label "Pacific Programme for the Elimination of Lymphatic Filariasis" \
  :description "Pacific Programme for the Elimination of Lymphatic Filariasis" \
  :definition < \
    :element -name "PacELF_ID" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
      < :description "Unique Identifier of the document" > \
    :element -name "type" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
      < :description "Type of document format. e.g. electronic or hard copy" > \
    :element -name "category" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
      < :description "Category representing the source of the document. e.g. journal, meeting notes, scientific paper" > \
    :element -name "hardcopy_location" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
      < :description "Physical location of the hardcopy." > \
    :element -name "title" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Title of the publication" > \
    :element -name "description" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "description of the document" > \
    :element -name "year" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
    	< :description "Year of publication" > \
    :element -name "authors" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Author(s) of the document" > \
    :element -name "journal" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Journal that published the document" > \
    :element -name "publisher" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Publisher of the document" > \
    :element -name "volume-issue" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Volume/Issue of the document" > \
    :element -name "pages" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Identifies relevant pages in document" > \
    :element -name "work_location" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Work Location" > \
    :element -name "access_rights" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Access rights to the document." > \
    :element -name "language" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Language" > \
    :element -name "pdf_file_name" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "PDF file name" > \
	:element -name "decade" -type "string" -comparable "true" -min-occurs "0" -max-occurs "1" \
	    < :description "Decade Research Took Place In" > \
  >

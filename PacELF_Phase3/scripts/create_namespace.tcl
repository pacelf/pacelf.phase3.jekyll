#=================================================================================
#
# Package to ingest PacELF data within Mediaflux
#
# Note: this is in Development status.
#
#    2.0   Collin Storlie 09 May 2018
#
#    This is the first script to run
#
#=================================================================================

# set some constants
# NAMESPACE is where the documents will reside within Mediaflux storage on the rdsi server

set NAMESPACE   "/rdsi/TDH/PacELF_Phase3"

# Check if the namespace exists, if not, create the project

if { [ xvalue "exists" [ asset.namespace.exists :namespace "$NAMESPACE" ]] == "false" } {
	asset.project.create :description "Pacific Programme for the Elimination of Lymphatic Filariasis" :name "PacELF_Phase3" :namespace "/rdsi/TDH" \
		:metadata-namespace "true" \
		:dictionary-namespace "true" \
		:project-roles < :administrator < :actor -type "user" "system:manager" > \
										 :visitor < :actor -type "user" "portal:anonymous" > > \
		:quota < :allocation 5000MB :description "limited to 5 GB" :owner < :domain "system" :name "manager" > >
}
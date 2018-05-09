#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
from crossref.filters import works_examples as we
"""

has_funder = 'has-funder:t' #Requires t, true, 1, f, false 0

#JAH: This is a work in progress
#???? What is an example funder that is returned from works?
#National Cancer Institue found by using Funders endpoint
funder = 'funder:100000054'

location = 'location'
prefix = 'prefix'
member = 'member'

#-------  Dates --------
from_index_date = 'from-index-date'
until_index_date	= 'until-index-date'
from_deposit_date = 'from-deposit-date'	#{date}	metadata last (re)deposited since (inclusive) {date}
until_deposit_date	 = 'until-deposit-date'   #{date}	metadata last (re)deposited before (inclusive) {date}
from_update_date = 'from-update-date'	#{date}	Metadata updated since (inclusive) {date}. Currently the same as from-deposit-date.
until_update_date = 'until-update-date'	            #{date}	Metadata updated before (inclusive) {date}. Currently the same as until-deposit-date.
from_created_date	= 'from-created-date:2018-01-15'   #{date}	metadata first deposited since (inclusive) {date}
until_created_date	 = 'until-created-date'	    #{date}	metadata first deposited before (inclusive) {date}
from_pub_date = 'from-pub-date'	    #{date}	metadata where published date is since (inclusive) {date}
until_pub_date = 'until-pub-date'	  #{date}	metadata where published date is before (inclusive) {date}
from_online_pub_date = 'from-online-pub-date'	  #{date}	metadata where online published date is since (inclusive) {date}
until_online_pub_date = 'until-online-pub-date'     	#{date}	metadata where online published date is before (inclusive) {date}
from_print_pub_date = 'from-print-pub-date'	#{date}	metadata where print published date is since (inclusive) {date}
until_print_pub_date = 'until-print-pub-date'   	#{date}	metadata where print published date is before (inclusive) {date}
from_posted_date = 'from-posted-date'   #{date}	metadata where posted date is since (inclusive) {date}
until_posted_date	= 'until-posted-date'  #{date}	metadata where posted date is before (inclusive) {date}
from_accepted_date	 = 'from-accepted-date'     #{date}	metadata where accepted date is since (inclusive) {date}
until_accepted_date = 'until-accepted-date'	#{date}	metadata where accepted date is before (inclusive) {date}

#------ License-----------
has_license = 'has-license'		    #metadata that includes any <license_ref> elements.
license_url = 'license.url'	        #{url}	metadata where <license_ref> value equals {url}
license_version = 'license.version'	   #{string}	metadata where the <license_ref>'s applies_to attribute is {string}
license_delay	 = 'license.delay'      #{integer}	metadata where difference between publication date and the <license_ref>'s start_date attribute is <= {integer} (in days)

#------ Full Text -------
has_full_text	= 'has-full-text'	#metadata that includes any full text <resource> elements.
full_text_version = 'full-text.version'	#{string}	metadata where <resource> element's content_version attribute is {string}.
full_text_type = 'full-text.type'	#{mime_type}	metadata where <resource> element's content_type attribute is {mime_type} (e.g. application/pdf).
full_text_application = 'full-text.application'	#{string}	metadata where <resource> link has one of the following intended applications: text-mining, similarity-checking or unspecified

#------- Others -------
has_references = 'has-references'		#metadata for works that have a list of references
reference_visibility = 'reference-visibility' 	#[open, limited, closed]	metadata for works where references are either open, limited (to Metadata Plus subscribers) or closed
has_archive = 'has-archive'		#metadata which include name of archive partner
archive = 'archive'    #{string}	metadata which where value of archive partner is {string}

#------- IDs ---------
has_orcid	 = 'has-orcid'	#metadata which includes one or more ORCIDs
has_authenticated_orcid = 'has-authenticated-orcid'	#	metadata which includes one or more ORCIDs where the depositing publisher claims to have witness the ORCID owner authenticate with ORCID
orcid = 'orcid'	#{orcid}	metadata where <orcid> element's value = {orcid}
issn	= 'issn'   #{issn}	metadata where record has an ISSN = {issn}. Format is xxxx-xxxx.
isbn	= 'isbn'  #{isbn}	metadata where record has an ISBN = {issn}.
directory = 'directory' #	{directory}	metadata records whose article or serial are mentioned in the given {directory}. 
                #Currently the only supported value is doaj.
doi = 'doi'	 #{doi}	metadata describing the DOI {doi}
updates = 'updates'	#{doi}	metadata for records that represent editorial updates to the DOI {doi}
is_update	 = 'is-update'	#metadata for records that represent editorial updates
has_update_policy = 'has-update-policy'	#	metadata for records that include a link to an editorial update policy
container_title = 'container-title'	#	metadata for records with a publication title exactly with an exact match
category_name	= 'category-name' #	metadata for records with an exact matching category label. Category labels come from this list published by Scopus
type_id = 'type'  #{type}	metadata records whose type = {type}. Type must be an ID value from the list of types returned by the /types resource
type_name	 = 'type-name'	#metadata for records with an exacty matching type label
award_number = 'award.number'	#{award_number}	metadata for records with a matching award nunber. Optionally combine with award.funder
award_funder = 'award.funder' #{funder doi or id}	metadata for records with an award with matching funder. Optionally combine with award.number
has_assertion	= 'has-assertion'	#metadata for records with any assertions
assertion_group = 'assertion-group'	#	metadata for records with an assertion in a particular group
assertion = 'assertion'		#metadata for records with a particular named assertion
has_affiliation = 'has-affiliation'      #		metadata for records that have any affiliation information
alternative_id = 'alternative-id'    #		metadata for records with the given alternative ID, which may be a publisher-specific ID, or any other identifier a publisher may have provided
article_number = 'article-number'   #		metadata for records with a given article number
has_abstract = 'has-abstract'	 #	metadata for records which include an abstract
has_clinical_trial_number = 'has-clinical-trial-number'	#	metadata for records which include a clinical trial number
content_domain = 'content-domain'		#metadata where the publisher records a particular domain name as the location Crossmark content will appear
has_content_domain	 = 'as-content-domain'		#metadata where the publisher records a domain name location for Crossmark content
has_domain_restriction = 'has-domain-restriction'	#	metadata where the publisher restricts Crossmark usage to content domains
has_relation = 'has-relation'	#metadata for records that either assert or are the object of a relation
relation_type = 'relation.type'		#One of the relation types from the Crossref relations schema (e.g. is-referenced-by, is-parent-of, is-preprint-of)
relation_object = 'relation.object'		#Relations where the object identifier matches the identifier provided
relation_object_type = 'relation.object-type'	#	One of the identifier types from the Crossref relations schema (e.g. doi, issn)



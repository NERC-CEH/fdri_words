# Metadata Catalogue Overview
A high-level overview of the servers and services required to run the EIDC metadata catalogue.

![](Catalogue.drawio.svg)
## Related services

- **a.** Search indexing service for metadata documents and vocabularies required by metadata editor.
- **b.** Web Map Service (WMS) editing and display.
- **c.** Metadata records link to datasets hosted by Data Packager.
- **d.** Data Packager servers up zipped files from the SAN.
- **e.** Direct access to files on the SAN.
- **f.** Proxy controls access to the catalogue. Provides authentication and user registration services.
- **g.** Crowd provides combined user and group management. Authentication and authorization services.
- **h.** Authentication to the catalogue.
- **i.** Hubbub file upload and management. Uploads files directly to the SAN.
- **j.** Hubbub data stored in Postgres.
- **k.** Metadata records are configured to use Order Manager for order processing. Order processing is managed by the
Licensing Team.
- **l.** Order Manager data stored in Mongodb.
- **m.** All public metadata records exported to Fuseki triple store.
- **n.** Legilo provides analysis services to the metadata editor, finds keywords and observed properties in the
supporting documentation.
- **o.** Jira integrates with the file upload process during the ingestion process.
- **p.** FME processes orders for Order Manager. Job management.
- **q.** Data store
- **r.** Catalogue uploads files directly to datastore dropbox.
- **s.** Legiolo uses OpenAI LLM's to extract potential observed properties from the supporting documentation.
- **t.** The EIDC website is the entry point to the catalogue.
- **u.** Catalogue editor uses vocabularies stored on the Skosmos server, loads them at startup.
- **v.** Catalogue loads vocabularies from external sources at startup.
- **w.** DOI registration service, DataCite.
- **x.** Catalogue editor imports method metadata from GitHub.
- **y.** New user interface element hosting for Spatial Explores and Data Preview.
 
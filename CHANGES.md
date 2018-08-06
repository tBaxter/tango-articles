# Tango Articles Change Log

## 0.13.0
* Django 2.0 and Python 3.x compatible
* Removed comments dependency
* Fixed get_absolute_url syntax
* Formally require typogrify
* Corrected and updated tests
* Removed permalink references
* Reduced dependency on tango-photos
* Added migrations


## 0.12.2
* Removed deprecated assignement_tag

## 0.12.1
* Additional fixes for Django 2.0

## 0.12.0
* Adopted Django 2.0 URL syntax

## 0.11.2
* Additional on_delete arguments for 2.0 compatibilty

## 0.11.1
* Added on_delete argument for 2.0 compatibilty

## 0.11.0
* Recovered long-lost LinkRoll models.

## 0.10.1
* Added check for presence of tango_admin

## 0.10.0
* Changes for Django 1.8+

## 0.9.0
* Added attachments to articles

## 0.8.1
* Added classifiers to setup.py

## 0.8.0
* Updates for Travis, Django 1.8 and Python 3

## 0.7.2
* Minor changes for Django 1.8

## 0.7.1
* Updated h-entry microformat tags

## 0.7.0
* Updates for Django 1.7
* Moved admin media definitions out. Now supported by tango-admin.

## 0.6.0
* Stubbed base URLs

## 0.5.4
* Comment recovery

## 0.5.3
* Articles list images resolve correctly

## 0.5.2
* Articles list now defaults to destination_slug 'articles', so the url /articles/ or /news/ returns all articles with the destination 'articles' (assuming no more specific destination is wanted)

## 0.5.1
* Corrected bad template tag in article detail

## 0.5
* No more calls to markup
* Improved how-to documentation
* Removed redundant dependencies

## 0.4.1
* Removed requirements satisfied by tango-shared
* Improved hnew microformatting in article details

### 0.4
* Drag and drop ordering of article images
* Bulk photo uploading
* Improved article detail templates
* Clearer blog and article entry forms
* Tentative Python 3 support
* Django 1.6 support

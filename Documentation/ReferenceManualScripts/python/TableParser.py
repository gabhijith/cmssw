# email: cmsdoxy@cern.ch, ali.mehmet.altundag@cern.ch

# please have a look at the namespaces.html (namespace list) and annotated.html
# (~class list) html files to understand the tags/attributes that we use in
# this script.

from bs4 import BeautifulSoup
import sys, os, copy

htmlFullPath     = None
htmlFilePath     = None
htmlFileName     = None
fileNameTemplate = None # html file name template
htmlPage         = None
tableClassName   = 'directory'

# load rows from the table in [C]lass and [N]amespace list pages  and prapere
# pages in the following structure: pages = {'A' : [...], 'B' : [...]}
def extractPages(configFileFlag = False):
    # initial page, A
    pages = {'A':[]}
    # find all class/namespace talbe rows.
    table = htmlPage.find('table', {'class' : tableClassName})
    for row in table.findAll('tr'):
        # please see the related html file (annotated.html) to understand the
        # approach here. you will see that, only hidden rows have style
        # attribute and these hidden rows must be added to pages of their
        # parents. This is why we need to check whether row has a style
        # attribute or not.
        styleFlag = False
        if 'style' in row: styleFlag = True
        # change the first letter if row is not hidden (child) one
        if not styleFlag: firstLetter = row.findAll('td')[0].text[0].upper()
        # if pages dict doesn't have the page yet..
        if firstLetter not in pages:
            pages[firstLetter] = []
        # insert the row into the related page
        if configFileFlag:
            url = row.find('a')['href']
            if '_cff' in url or '_cfi' in url or '_cfg' in url:
                pages[firstLetter].append(row)
        else:
            pages[firstLetter].append(row)
    return pages

# load rows from the package documentation page. output structure:
# pages = {'PackageA' : [..], 'PackageB' : [...]}
def extractPagesForPackage():
    # initial page, A
    pages = {}
    table = htmlPage.find('table', {'class' : tableClassName})
    for row in table.findAll('tr'):
        # first cell contains name of the package...
        name = row.findAll('td')[0].text
        # parse package names --please have a look at the pages.html file
        name = name[name.find(' '):name.find('/')].strip()
        # if the package is not added yet
        if name not in pages: pages[name] = []
        pages[name].append(row)
    return pages

# generate alphabetic tab for html pages that will be generated by this script
def generateTab(items, curr, tabClass = 'tabs3'):
    itemTagMap = {}; tab = ''
    for item in items:
        fn  = fileNameTemplate % item.replace(' ', '') # generate file name
        if item != curr: tab += '<li><a href="%s">%s</a></li>' % (fn, item)
        else: tab += '<li class="current"><a href="%s">%s</a></li>'%(fn, item)
    return '<div class="%s"><ul class="tablist">%s</ul></div>' % (tabClass,tab)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("not enough parameter!\n")
        sys.exit(1)

    # initialize variables
    htmlFullPath     = sys.argv[1]
    htmlFilePath     = os.path.split(htmlFullPath)[0]
    htmlFileName     = os.path.split(htmlFullPath)[1]
    fileNameTemplate = htmlFileName.replace('.html', '_%s.html')

    # load the html page
    with open(htmlFullPath) as f:
        htmlPage = f.read()
        htmlPage = BeautifulSoup(htmlPage)

    # please have a look at the pages.html page. You will see that class name
    # of the related tab, which we will use to put 'index tab' by using this
    # tab, is different for pages.html file. For namespaces.html (namespace
    # list) and annotated.html (~class list) files, class names are the same
    # tabs2. this is why we are setting 'the destination tab class name' up
    # differently depending on the html file name.
    if htmlFileName == 'packageDocumentation.html':
        pages = extractPagesForPackage()
        destTabClassName = 'tabs'
    elif htmlFileName == 'configfiles.html':
        pages = extractPages(configFileFlag = True)
        destTabClassName = 'tabs2'
    else:
        pages = extractPages()
        destTabClassName = 'tabs2'

    allRows = []
    pageNames = pages.keys(); pageNames.sort()
    for page in pageNames:
        allRows = allRows + pages[page]
    pages['All'] = allRows
    pageNames.append('All')

    # prepare the template
    table     = htmlPage.find('table', {'class' : tableClassName})
    # generate template (clean whole table content)
    for row in table.findAll('tr'):
        row.extract()

    # generate pages
    for page in pageNames:
        print('generating %s...' % (fileNameTemplate % page))
        temp   = BeautifulSoup(str(htmlPage))
        table  = temp.find('table', {'class' : tableClassName})
        oldTab = temp.find('div', {'class' : destTabClassName})
        newTab = generateTab(pageNames, page)
        oldTab.replaceWith(BeautifulSoup(oldTab.prettify() + str(newTab)))
        for row in pages[page]:
            table.append(row)
        # replace blank character with '_'. Please notice that you will not
        # be able to use original page name after this line.
        page = page.replace(' ', '_')
        with open('%s/%s'%(htmlFilePath, fileNameTemplate % page), 'w') as f:
            f.write(str(temp))

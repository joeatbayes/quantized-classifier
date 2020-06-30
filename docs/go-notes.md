# Notes on Go made while developing classifier

## Tools

- [LiteIde](https://sourceforge.net/projects/liteide/?source=typ_redirect) - GO editor with good color and auto suggest on windows.   I love this editor it does just enough completion to be useful and does a good job colorizing without creating a lot of extra artifacts.   I still do my compiling in a shell window.    
- [List of GO Editors](https://github.com/golang/go/wiki/IDEsAndTextEditorPlugins)
- I tried [ATOM](https://atom.io/) but it kept crashing and occasionally lost content.
- [Typora Visual Markdown Editor](https://typora.io/)  An immense time saver when editing markdown especially when you want to use tables.   

## Go Tutorial & Introduction

- [How to Write GO Code](https://golang.org/doc/code.html)
- [Go Blog](https://blog.golang.org/gos-declaration-syntax) - Good samples of most basic Go coding
- [Organizing code for Multi-file projects](https://golang.org/doc/code.html)
- [GoLang for Everyone](https://www.goinggo.net/2014/03/exportedunexported-identifiers-in-go.html) - Exported / Unexported Identifiers William        Kennedy some good examples [Reducing Type Hierarchies](https://www.goinggo.net/2016/10/reducing-type-hierarchies.html) [Composition with Go](https://www.goinggo.net/2015/09/composition-with-go.html)  [OOP semantics in GO](https://www.goinggo.net/2015/09/composition-with-go.html)   
- [Effective Go](https://golang.org/doc/effective_go.html) -  Re-read this as a style guide every so often.

## Specific Features / Tasks in Go

- [GO Package List](https://golang.org/pkg/)

- [Go Lang Book](https://www.golang-book.com/books/intro/6)

- - [Arrays, Slices and Maps](https://www.golang-book.com/books/intro/6)
  - [Structs including initialization](https://www.golang-book.com/books/intro/9#section1)

- [Go Blog  Maps / Hash tables](https://blog.golang.org/go-maps-in-action) 

- [Go Declaration Syntax](https://blog.golang.org/gos-declaration-syntax)

- [DOC Structs and Interfaces](https://www.golang-book.com/books/intro/9)

- [Constants & enums in Go](https://andrey.nering.com.br/2016/constants-and-enums-in-go-lang/)

- [JSON go by example](https://gobyexample.com/json)

- [Writing Files GO by example](https://gobyexample.com/writing-files)  [GOFile Docs](https://golang.org/pkg/os/#File.WriteString)

- [Read Command Line Parameters](https://gobyexample.com/command-line-arguments)

- [Check if File or Dir Exists](https://gist.github.com/mattes/d13e273314c3b3ade33f)

- [Byte Buffer similar to StringBuilder](https://golang.org/pkg/bytes/#example_Buffer)

- [Return Multiple Values](https://gobyexample.com/multiple-return-values) 

- ..

- ..

# Hosting GO Servers 
Hosting go servers is problematic when using shared server hosting because most of the time when I write GO servers instead of Node it is because they maintain state like a machine learning engine.  This means they need to run for a long time and they can consume some non trivial memory.  

One way to do this is with specialized services who support GO hosting the other is with virtual private servers.  I prefer private month to month leased servers as they provide superior performance per dollar and give me CPU power that is guaranteed to be available when I need it.     My favorite is [CloudSouth.com](https://www.cloudsouth.com/dedicated-servers/). The minimum cost is about 50 dollars per month but you get dedicated performance with 16 Gig of Ram and 8 cores that deliver much better performance than the virtual core some big vendors quote.   For 69 dollars per month you get 32GB of RAM and 12 fast cores.  I have found these servers to cost about 1/10th per unit of peformance compared to AWS servers and their storage is cheap.    

> > > Don't get fleeced by the virtual server vendors.  If you are paying more than $45 per month for your server then you will probably obtain a better ROI,  better performance and better performance predictability using the month to month leaded servers from CloudSouth. 

The problem is many servers like our free Quantized Learning engine hosted it is hard to justify 69.00 per month when you may be paying to host it for years. 

### Configuring Go Server on a Bare Linux server:
TODO: Fill this in. 

### Partial List of Go server hosting Companies

* [Low End Virtual Box Serves](https://lowendbox.com/)

* [dngsolutions uk](https://dngsolutions.co.uk/billing/cart.php?a=confproduct&i=0)   5.6 GBP monthly for 2 cores, 4GB of ram, 50GB disk 2TB bandwidth.  This seems like the cheapest option for a server with enough muscle to run anything other than toys.  Note:  If you go to their current pricing through their menu the price is currently higher but if you use the embedded link they still seem to be honoring the better price.   5.6 GBP converts to 6.99 USD.

* [LinNode Hosting](https://www.linode.com/) Virtual private box for $10.00 per month get 2 GB Ram with 1 Core and 24 GB SSD.  At 80 dollars per month you get 12GB RAM, 6 Cores, 192GB of SSD storage.  

* [Digital Ocean](https://www.digitalocean.com/pricing/#droplet) Virtual box 10 dollars per month buys 1 GB memory,  1 Core, 30 GB SSD or for 20 dollars per month 2 GB of memory, 2 cores, 40 GB SSD Disk.   

* [Go in cloud by Clever Cloud](http://www.golang-cloud.com/en) Includes auto scaling.  Currently offering free trial as of Feb-3-2017 but would not show pricing. 

* [Instructions to run GO on Redhats OpenShift Platform](https://github.com/gcmurphy/golang-openshift)

* [Instructions to run GO servers on HeroKu](https://devcenter.heroku.com/articles/getting-started-with-go#introduction)  [Heroku pricing](https://www.heroku.com/pricing)  Free limited to 512MB ram,   7 dollars per month = 512MB ram,   Other pricing up to dedicated servers it lists 25 to 500 dollars per month but no details to really compare.   [Heroku buildpack for GO](https://github.com/heroku/heroku-buildpack-go)

* [Instructions to run GO servers on Google App Engine](https://blog.golang.org/go-and-google-app-engine)

* ​


# Using GO for Cloud Configuration
* [Configuring Go servers with Docker](https://blog.golang.org/docker)
* [Using GO to mnage Cloud Sigma Cloud](https://www.cloudsigma.com/using-cloudsigmas-api-with-golang/)



# Misc

- [Go performance tales](http://jmoiron.net/blog/go-performance-tales)
- [10 things you probably do not know about GO](https://talks.golang.org/2012/10things.slide#1)
- [Five things that make Go fast](https://dave.cheney.net/2014/06/07/five-things-that-make-go-fast)
- ​
- [Hashtable algorithm performance compared](http://incise.org/hash-table-benchmarks.html)
- A very fast hash table claims to be faster than a Judy array http://preshing.com/20130107/this-hash-table-is-faster-than-a-judy-array/


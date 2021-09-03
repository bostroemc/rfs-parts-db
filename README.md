# README job-queue

__rfs-parts-db__ handles a parts database for a rollfeed system. An interface to the ctrlX Data Layer is included.  It is based on the 
__datalayer.provider__ sample provided by ctrlX AUTOMATION SDK V1.8.

## Introduction

The app demonstrates how a Data Layer connection is established and a node is provided.

## Prerequisites for Developing python Apps

* Linux Ubuntu 18.4 (or Windows PC running with Windows Subsystem for Linux (WSL) or a Virtual Box VM)
* Python3 is installed 
* ctrlX AUTOMATION SDK Version 1.8 is installed (extracted and copied to the Ubuntu users home directory)

## Getting Started

### Install Test Environment

* Create and install a ctrlX CORE<sup>virtual</sup> or use actrlX CORE if available.

If your Linux Ubuntu has NO direct internet access you need a proxy server and you need to provide the proxy server settings to the development tools. In this description we assume that under the address 127.0.0.1:3128 a proxy server is running, providing both http and https access.

In this case change to your home directory (~), open the file .bashrc and add these lines:

export http_proxy=http://127.0.0.0:3128
export https_proxy=http://127.0.0.1:3128  

### Install Local Development Environment
We recommend to install a virtual python environment for developing python apps.

1. Start a shell and change to this folder.
2. Create a virtual (isolated) python environment: `virtualenv -p python3 venv`
3. Activate the environment: `source venv/bin/activate`
4. Install the datalayer C++/python wrapper files (substitute xxx with the right version): `pip3 install ../../whl/ctrlx_datalayer-xxx-py3-none-any.whl`
5. Install the ctrlX Flattbuffers python files (substitute xxx with the right version): `pip3 install ../../whl/ctrlx_fbs-xxx-py3-none-any.whl`


Hint: If you want to install further python packages from the internet and you are behind a proxy then add the proxy settings to your pip3 install command e.g. `pip3 install --proxy localhost:3128 flatbuffers`.

### Build AMD64 Snap
1. Start a shell and change to this folder.
2. Remove the virtual environment folder: `rm -r venv`
3. Reset snapcraft build artifacts: `snapcraft clean`
4. Build the snap (see hints): `snapcraft` 

Hints:

The build of python ARM64 snaps will be supported in the upcomming release in July 2021. As a workaround you can use a native ARM86 machine.

Install your virtual python environment again - see previous chapter.

### Install the Snap on the ctrlX

* Open the ctrlX CORE Home page, select Settings - Apps, click on 'Service mode' and confirm.
* Click on the Settings icon and select 'Allow installation from unknown source'
* Select tab 'Local storage', click the + icon, upload and install the snap.
* Switch to Operation mode

## Troubleshooting

* If your snap doesn't work well start a shell on the ctrlX and check the trace regarding your snap: `$ sudo snap logs -f rexroth-python-provider`

## Support

If you've any questions visit the [ctrlX AUTOMATION Communitiy](https://developer.community.boschrexroth.com/)

___

## License

MIT License

Copyright (c) 2020, Bosch Rexroth AG

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
# datalayer-provider

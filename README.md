# ANSA TOOLS PACKAGE

This package is a tools-package for ANSA(a CAE preprocess software)
These enhancements make access much easier, and also debugging! This module was written for the reason, that the common scripting API did not feel pythonic enough to me. 

Authors: Xinxing.Zhang
[Contact Author](WeChat:zxx4477 Email:zxx4477@126.com)

# Installation

Just copy the fles into your installation folder: */BETA_CAE_Systems/shared_v23.1.0/python/win64/Lib/site-packages

# Example

	matlib=MaterialLibrary();
    matlib.createSqlTable();
    matlib.cleanAllTableData();
    matlib.importDataToSqlite();
    matlib.helpinfo()
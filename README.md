# Clone the repository
```
git clone git@github.com:chidie/p4d-remoteops-utils.git
cd p4d-remoteops-utils
```
# Create a virtual environment using 
```python -m venv venv
   venv/Scripts/Activate.ps1    # On windows 
```
# Install dependencies
```
    pip install -r requirements.txt
```

>Note: Paste correct GXW3OpenIF32.dll in the /dll folder or any desired location in your PC. 

# Paste DLL file path in the main.py file and run the file.

>NOTE: Due to Windows security policies, DLLs downloaded from the internet or network locations are often "blocked."
- Place GXW3OpenIF64.dll in the ````/dll```` folder or any desired location in your PC.
- Unblock the DLL
    * Right-click on GXW3OpenIF64.dll -> Properties
    * Check the *Unblock* checkbox at the bottom of the General tab.
    * Click on Apply and OK

> NOTE: Key libraries like Paramiko is for SFTP communication and pythonnet is for loading .DLL file.

## Task 1: 
- Check whether 'path' points to an existing regular folder on the remote host.
- Symbolic links, shortcuts, files or non-existent paths return False
>Note: A Windows junction pointing to an existing folder is treated as a folder

## Task 2: 
- Create the folder at 'folder_path' and any missing parent folders on the remote host.
  * If 'folder_path' already exists and is a folder, nothing happens.
  * If it exists and is NOT a folder, an exception is raised.
>NOTE: The 'create_folder_path_recursively' method does not delete, modify, or overwrite existing filesystem instances.


# Errors encountered and solutions:
>ERROR 1: A .NET security error due to a direct download of the DLL test file from the internet.
```bash
    Failed to load DLL: Could not load file or assembly 'file:///C:\Users\chidi\Documents\test-dll-files\GXW3OpenIF64.dll' or one of its dependencies. Operation is not supported. (Exception from HRESULT: 0x80131515)
File name: 'file:///C:\Users\chidi\Documents\test-dll-files\GXW3OpenIF64.dll' ---> System.NotSupportedException: An attempt was made to load an assembly from a network location which would have caused the assembly to be sandboxed in previous versions of the .NET Framework. This release of the .NET Framework does not enable CAS policy by default, so this load may be dangerous. If this load is not intended to sandbox the assembly, please enable the loadFromRemoteSources switch. See http://go.microsoft.com/fwlink/?LinkId=155569 for more information.
   at System.Reflection.RuntimeAssembly._nLoad(AssemblyName fileName, String codeBase, Evidence assemblySecurity, RuntimeAssembly locationHint, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
   at System.Reflection.RuntimeAssembly.InternalLoadAssemblyName(AssemblyName assemblyRef, Evidence assemblySecurity, RuntimeAssembly reqAssembly, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
untimeAssembly reqAssembly, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
Introspection, Boolean suppressSecurityChecks)
   at System.Reflection.RuntimeAssembly.InternalLoadFrom(String assemblyFile, Evidence securityEvidence, Byte[] hashValue, AssemblyHashAlgorithm hashAlgorithm, Boolean forIntrospection, Boolean suppressSecurityChecks, StackCrawlMark& stackMark)
   at System.Reflection.Assembly.LoadFrom(String assemblyFile)
   at Python.Runtime.AssemblyManager.LoadAssemblyPath(String name)
   at Python.Runtime.CLRModule.AddReference(String name)
```
### Here is the fix:
- Open the DLL file location, right-click on it and select *properties*
- At the bottom of the *General* tab, you will find a security warning: *"This file came from another and might be blocked to help protect ..."*
- Check the *Unblock* checkbox and click *Apply* and *OK*

>ERROR 2: Architecture Mismatch error - Using a 32-bit DLL file on a 64-bit Python environment. Use GXW3OpenIF32.dll for a 32-bit Python environment and GXW3OpenIF64.dll for a 64-bit Python environment.
```
Failed to load DLL: Could not load file or assembly 'file:///C:\Users\chidi\Documents\test-dll-files\GXW3OpenIF32.dll' or one of its dependencies. An attempt was made to load a program with an incorrect format.
File name: 'file:///C:\Users\chidi\Documents\test-dll-files\GXW3OpenIF32.dll'
   at System.Reflection.RuntimeAssembly._nLoad(AssemblyName fileName, String codeBase, Evidence assemblySecurity, RuntimeAssembly locationHint, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
   at System.Reflection.RuntimeAssembly.InternalLoadAssemblyName(AssemblyName assemblyRef, Evidence assemblySecurity, RuntimeAssembly reqAssembly, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
   at System.Reflection.RuntimeAssembly.InternalLoadFrom(String assemblyFile, Evidence securityEvidence, Byte[] hashValue, AssemblyHashAlgorithm hashAlgorithm, Boolean forIntrospection, Boolean suppressSecurityChecks, St   at System.Reflection.RuntimeAssembly._nLoad(AssemblyName fileName, String codeBase, Evidence assemblySecurity, RuntimeAssembly locationHint, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
   at System.Reflection.RuntimeAssembly.InternalLoadAssemblyName(AssemblyName assemblyRef, Evidence assemblySecurity, RuntimeAssembly reqAssembly, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
   at System.Reflection.RuntimeAssembly.InternalLoadAssemblyName(AssemblyName assemblyRef, Evidence assemblySecurity, RuntimeAssembly reqAssembly, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
   at System.Reflection.RuntimeAssembly.InternalLoadFrom(String assemblyFile, Evidence securityEvidence, Byte[] hashValue, AssemblyHashAlgorithm hashAlgorithm, Boolean forIntrospection, Boolean suppressSecurityChecks, St   at System.Reflection.RuntimeAssembly.InternalLoadFrom(String assemblyFile, Evidence securityEvidence, Byte[] hashValue, AssemblyHashAlgorithm hashAlgorithm, Boolean forIntrospection, Boolean suppressSecurityChecks, StackCrawlMark& stackMark)
   at System.Reflection.Assembly.LoadFrom(String assemblyFile)
   at Python.Runtime.AssemblyManager.LoadAssemblyFullPath(String name)
   at Python.Runtime.CLRModule.AddReference(String name)
```

### Here is the fix: 
- Simply replace the 32-bit DLL test file with 64-bit version or vice-versa depending on your Python environment
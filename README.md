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

## Task Overview

### Task 1: Remote Filesystem Inspection Logic
**Objective:** Implement a robust mechanism to validate remote filesystem entities via SFTP.
* Developed `is_path_a_regular_folder` to distinguish between actual directories and "noise" (files, symbolic links, or shortcuts).
* Utilized `lstat` to prevent the accidental following of symlinks, ensuring the integrity of the "regular folder" requirement.
* Normalized path separators to ensure functionality across both Linux and Windows remote hosts.

### Task 2: Recursive Remote Directory Management
**Objective:** Create a fail-safe, recursive folder creation utility.
* Implemented `create_folder_path_recursively` to build complex path structures level-by-level.
* Integrated type-checking at every level of the recursion to prevent directory creation if a file with the same name already exists.
* Designed the method to return an integer count of successfully created folders for audit and testing purposes.

### Task 3: 64-bit .NET Assembly Interoperability
**Objective:** To bridge the gap between Python and managed 64-bit DLL file(`GXW3OpenIF64.dll`).
* Leveraged `pythonnet` (CLR) to load the Mitsubishi Electric assembly into the Python process.
* Verified architecture compatibility to ensure 64-bit Python communicates correctly with 64-bit binaries (preventing "Incorrect Format" errors).

### Task 4: Dynamic API Discovery (Reflection)
**Objective:** To automatically map the available functionality of the Mitsubishi Factory interface.
* Used Python's reflection capabilities (`dir`, `getattr`, `callable`) to filter out standard .NET boilerplate and isolate unique business logic methods.
* Implemented a "Deep Inspection" strategy to navigate from the Factory class to the functional `Instance` object where the project-management methods reside.

### Task 5: Managed Security & Trust Configuration
**Objective:** To resolve .NET security issues.
* Documented and implemented fixes.
* Wrapped the entire loading sequence in specific exception handlers to provide actionable feedback for OS-level and Runtime-level failures.

### Task 6: Enterprise-Grade Logging and Structure
**Objective:** To transition from "scripts" to a maintainable software package.
* Adopted seperation of concerns technique, added the `src/` layout to separate library logic from execution scripts.

# Errors encountered and fixes:
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
fixe- Check the *Unblock* checkbox and click *Apply* and *OK*

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
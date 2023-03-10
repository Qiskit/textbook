# Qiskit Textbook Translation Release Guide

This file shows the steps of how to release your translated and merged files.

## The first time when you release the translation
1. Copy [toc.yaml](https://github.com/Qiskit/platypus/blob/main/notebooks/toc.yaml) file from `./notebooks/` and paste it under your language folder `./translations/xx/`.
2. In toc.yaml file, keep only lines about translated and merged files and remove the rest. 
    - Example: if only the file `/ch-states/representing-qubit-states` was merged, please keep below lines and remove the rest of the files.
```
- title: Quantum States and Qubits
  url: /ch-states
  sections:
    - title: Representing Qubit States
      id: representing-qubit-states
      uuid: b81717ca-b519-11ec-b909-0242ac120002
      url: /ch-states/representing-qubit-states
```      
3. Translate the titles of the folders. 
    - Example: translate `- title: Quantum States and Qubits` to `- title: 量子状態と量子ビット`
4. Remove the title lines of the file. Example: delete `    - title: Representing Qubit States`
5. Add `-` in front of `id`. Example: change `     id: representing-qubit-states` to `    - id: representing-qubit-states`
6. Example should look like:
```
- title: 量子状態と量子ビット
  url: /ch-states
  sections:
    - id: representing-qubit-states
      uuid: b81717ca-b519-11ec-b909-0242ac120002
      url: /ch-states/representing-qubit-states
```      
7. Commit the changes and send Pull Request.

Please see [toc.yaml for Japanese](https://github.com/Qiskit/platypus/blob/main/translations/ja/toc.yaml) for your reference.

## For second and subsequent release
When the new translated files are merged, update toc.yaml file as follows.
1. Copy the lines about new translated and merged files of [toc.yaml](https://github.com/Qiskit/platypus/blob/main/notebooks/toc.yaml) file under `./notebooks/`.
2. Paste it in the correct position of your toc.yaml file under your language folder `./translations/xx/`.
3. Translate the titles of the folders if you need.
4. Remove the title lines of the file if it exists.
5. Add `-` in front of `id`.
6. Example: If the file `/ch-states/case-for-quantum` was newly merged, then `toc.yaml` should be changed like
```
- title: 量子状態と量子ビット
  url: /ch-states
  sections:
    - id: representing-qubit-states
      uuid: b81717ca-b519-11ec-b909-0242ac120002
      url: /ch-states/representing-qubit-states
    - id: the-case-for-quantum-computers
      uuid: c0bbff62-b519-11ec-b909-0242ac120002
      url: /ch-states/case-for-quantum
```  
6. Commit the changes and send Pull Request.



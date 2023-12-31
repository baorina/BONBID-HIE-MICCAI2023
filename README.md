# BONBID-HIE 2023 release for MICCAI 2023
Challanege website: https://bonbid-hie2023.grand-challenge.org/bonbid-hie2023/

Dataset download: https://zenodo.org/record/8104103

Preprint paper: https://www.biorxiv.org/content/10.1101/2023.06.30.546841v1.abstract

@article{bao2023boston,\
  title={BOston Neonatal Brain Injury Dataset for Hypoxic Ischemic Encephalopathy (BONBID-HIE): Part I. MRI and Manual Lesion Annotation},\
  author={Bao, Rina and Song, Ya'nan and Bates, Sara V and Weiss, Rebecca J and Foster, Anna N and Cobos, Camilo Jaimes and Sotardi, Susan and Zhang, Yue and Gollub, Randy L and Grant, P Ellen and others},\
  journal={bioRxiv},\
  pages={2023--06},\
  year={2023},\
  publisher={Cold Spring Harbor Laboratory}\
}

BOston Neonatal Brain Injury Dataset for Hypoxic Ischemic Encephalopathy (BONBID-HIE): Part I. MRI and Manual Lesion Annotation

Hypoxic ischemic encephalopathy (HIE) is a brain injury that occurs in 1 ∼ 5/1000 term neonates. 
Accurate identification and segmentation of HIE-related lesions in neonatal brain magnetic resonance images (MRIs) 
is the first step toward predicting prognosis, identifying high-risk patients, and evaluating treatment effects.
It will lead to a more accurate estimation of prognosis, a better understanding of neurological symptoms, and a 
timely prediction of response to therapy. We release the first public dataset containing neonatal brain diffusion 
MRI and expert annotation of lesions from 133 patients diagnosed with HIE. HIE-related lesions in brain MRI are 
often diffuse (i.e., multi-focal), and small (over half the patients in our data having lesions occupying <1% of brain volume). 
Segmentation for HIE MRI data is remarkably different from, and arguably more challenging than, other segmentation 
tasks such as brain tumors with focal and relatively large lesions. We hope that this dataset can help fuel the 
development of MRI lesion segmentation methods for HIE and small diffuse lesions in general.

Contact:
Rina Bao: Rina.Bao@childrens.harvard.edu
Yangming Ou: Yangming.Ou@childrens.harvard.edu

License:
All training data has been made publicly available under the CC BY NC license (https://creativecommons.org/licenses/by-nc/4.0/legalcode.en), allowing academic use with credit, prohibiting commercial use without owner’s permission). 

Dockers for participating teams:

--bonbidhie_eval: evaluation docker for BONBID-HIE MICCAI 2023 Challenge. 

--bonbidhie2023_algorithms: algorithms demo docker for BONBID-HIE MICCAI 2023 Challenge.

For using these dockers, please read the README.md in each folder.

@echo off
echo PHASE3_PE_RESOURCE_OK>PHASE3.OK
imgmount a c:\DISK.IMA -t floppy
if exist a:\IMAGE.OK echo PHASE3_INTERNAL_DISK_IMAGE_OK>PHASE3.IMG
exit

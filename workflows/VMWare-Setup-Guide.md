# VMware Ubuntu VM Setup Guide

## 0. Install VMware
1. Send an email to IT to request VMware software to be made available through the software centre for your machine.
   Something along the lines of:

    > For the FDRI project I need to make use of the "VMware" software for development. Please could you action the 
      following: 
    > - VMWare Workstation, Vagrant and Vagrant VMWare utility to be explicitly made available to install through the 
        Software Centre for the following laptops:
    >   - **My Name**:  **WLL-ABCDEF1**
    >   - To be placed in the Carbon Black exemption list (quote "IT Support Ticket 26229" for confirmation)

    (replace My Name and the computer tag with yours)

2. Once you've had confirmation from IT, install the VMware software from the software centre.

## 1. Create the Ubuntu VM
1. Download the Ubuntu ISO: https://ubuntu.com/
2. In VMware Workstation: Create New Virtual Machine > Use ISO image
3. Start the VM and complete Ubuntu's installation wizard.

## 2. Install VMware Tools
This enables copy/paste between virtual and host machine, shared folders, multi-monitor support, etc.
```bash
sudo apt update
sudo apt-get install open-vm-tools open-vm-tools-desktop
```
Reboot the VM after installing.

## 3. Set Up a Shared Folder (optional)
You can set up a shared folder to quickly share files between the virtual and host machine.

1. Make a directory on your **host** machine that you want to share
2. Make a directory on your **VM** to link, e.g. 
    ```bash
    mkdir /home/<username>/HostShare
    ```
3. Configure shared folder in VMware Workstation:
   - Go to: VM > Settings > Options > Shared Folders
   - Follow wizard to select a folder on your host machine
   - The host folder should appear at `/home/<username>/HostShare`

## 4. Git setup
1. Install Git
    ```bash
    sudo apt update
    sudo apt install git
    ```
2. Generate SSH Key for GitHub
    ```bash
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa_vmware_github
    ```
3. Add the public key to GitHub
   - Copy contents of `~/.ssh/id_rsa_vmware_github.pub`
   - Add to GitHub: Settings > SSH and GPG keys

## 5. Install Docker
1. Add Docker's GPG key. This is a security step that ensures any Docker packages you install are actually from Docker 
   and haven't been tampered with.

    ```bash
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    ```
2. Add Docker repository to apt-sources
    ```bash
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```
3. Install Docker
    ```bash
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
4. Test installation
    ```bash
    sudo docker run hello-world
    ```

5. Post-installation: Allow running Docker without sudo (optional, but useful for integration with software like 
   PyCharm)
    ```bash
    sudo usermod -aG docker $USER
    ```
    - Log out and back in.
    - Verify with: `docker run hello-world` (no sudo)

## 6. Install Localstack CLI

1. Install the pre-built binary
```
curl --output localstack-cli-4.11.1-linux-amd64-onefile.tar.gz \
    --location https://github.com/localstack/localstack-cli/releases/download/v4.11.1/localstack-cli-4.11.1-linux-amd64-onefile.tar.gz
```

2. Extract the LocalStack CLI from the terminal

```
sudo tar xvzf localstack-cli-4.11.1-linux-*-onefile.tar.gz -C /usr/local/bin
```

## 7. Setup AWS-Vault

See [https://github.com/NERC-CEH/fdri_words/blob/main/aws/aws-vault.md](https://github.com/NERC-CEH/fdri_words/blob/main/aws/aws-vault.md)

## Additional Recommendations

### Snapshots
- Take a baseline snapshot after completing the OS install + updates + core tools
- Take regular snapshots, particularly before major system changes

**Take snapshot**
- In VMware Workstation, go to VM > Snapshot > Take Snapshot
- Give it a meaningful name
- Click Take Snapshot.

**Revert to a snapshot**
- Open VM > Snapshot.
- Select the snapshot you want to revert to.

### VM Performance
Allocate sufficient RAM (8GB+ recommended for development) and consider allocating multiple CPU cores.

- Shut down the VM (not suspend)
- In VMware Workstation, right-click the VM > Settings
- Go to Memory
  - Set to 8 GB or more (12–16 GB recommended if host has plenty).
- Go to Processors
  - Set 2–4 cores depending on host capacity.

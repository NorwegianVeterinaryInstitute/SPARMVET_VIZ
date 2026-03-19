# Secure SSH Tunneling for Colleague Access

**Exported:** 2/27/2026 13:11:05  
**Link:** [https://gemini.google.com/gem/5b39c0c1ec73/033e47ab3e9a833c](https://gemini.google.com/gem/5b39c0c1ec73/033e47ab3e9a833c)

## Prompt:
Hi, what would I need to do to make one of my container server (not all) accessible via SSH tunnel to one of my colleagues?

## Response:
Home Server assistant said
--------------------------

Since your **GreyServer** environment is strictly locked to the `home` firewall zone and NordVPN Meshnet, the safest way to provide a colleague access to a _single_ container (without exposing your entire host or other services) is via a **targeted SSH Local Port Forward**.

Before we start, I need to confirm which service you want to share. Based on your manifest, your active services are:

*   **Homebox** (Port 3100)
*   **YouTrack** (Port 8080)
*   **AI** (Port 3101)

### The Strategy

We will use your existing SSH access (Port 22) to "tunnel" the specific container port from your Thinkpad to your colleague's local machine. This keeps the traffic encrypted and bypasses the need to open any new ports in your Fedora firewall.

* * *

### Step 1: Create a Limited Guest User

To follow the principle of least privilege, we should not give your colleague access to your main user (UID 1000). We will create a "restricted" user on your Fedora host that has no shell access but can maintain a tunnel.

**Run this command as root (or via sudo):**

```
sudo useradd -m -s /sbin/nologin tunnel-guest
```

**Would you like me to proceed with setting a password for this user and configuring the specific SSH restricted rules?**

* * *

### 📑 Manifest Update Block (Pending)

```
## 3. Networking & Security (Addendum)
* **Temporary Access:** SSH Tunneling enabled for user `tunnel-guest`.
* **Restriction:** Shell access disabled (`/sbin/nologin`).
```

## Prompt:
Hi already have a tunel forward for myself, but I do not want my colleague to be able to access my whole server only the specific service

## Response:
Home Server assistant said
--------------------------

Understood. Since you already have your own tunnel, we need to ensure your colleague's access is **sandboxed**. To protect the **GreyServer** architecture and your private data in `/mnt/GreyServer/data/`, we will use a **Match User** block in your SSH configuration.

This prevents them from seeing your other services (like Cockpit on 9090) or browsing your filesystem.

### Step 2: Lockdown via SSH Configuration

We will configure the `sshd_config` to allow **only** the specific port forwarding and deny everything else (no shell, no X11, no other ports).

**Run this command to edit your config:**

```
sudo nano /etc/ssh/sshd_config
```

**Add these lines to the very end of the file:**

```
Match User tunnel-guest
    AllowTcpForwarding yes
    X11Forwarding no
    PermitTTY no
    PermitOpen localhost:8080
    ForceCommand /usr/sbin/nologin
```

_(Note: I used **8080** for YouTrack as an example; change this to **3100** if they need Homebox)._

**Would you like me to show you the specific command your colleague needs to run on their machine to connect once you've saved this?**

* * *

### 📑 Manifest Update Block

```
## 3. Networking & Security (Updated)
* **Guest Access:** User `tunnel-guest` created for external collaboration.
* **Hardening:** `PermitOpen` restricted to localhost:[SERVICE_PORT] only.
* **Shell Policy:** `PermitTTY no` + `ForceCommand /usr/sbin/nologin`.
```

## Prompt:
Please just explain solutions possibles no code, not doing yet

## Response:
Home Server assistant said
--------------------------

I understand. Since we are in the "architectural" phase, let's look at the three most secure ways to let your colleague into a specific **GreyServer** container without giving them the keys to your entire Fedora host or your private data in `/mnt/GreyServer/`.

### 1\. Restricted SSH Port Forwarding (The "Tunnel")

This is the most direct method using your existing SSH setup on Port 22.

*   **How it works:** You create a specific guest user on the host. In the SSH configuration, you use a `PermitOpen` rule.
*   **The "Wall":** This rule tells the server: "If this specific person logs in, only allow them to map **Port 8080** (or whichever service you choose) to their own computer."
*   **Result:** They can open `localhost:8080` in their browser, but if they try to SSH into your command line or access your Cockpit (9090), the server will instantly reject them.

### 2\. NordVPN Meshnet Permissions

Since you are already using Meshnet (`100.64.0.0/10`), you can leverage its built-in "Local network access" toggle.

*   **How it works:** You invite your colleague's NordVPN account to your Meshnet.
*   **The "Wall":** Instead of allowing "Full Access," you only route traffic to the specific IP and Port of the container.
*   **Result:** This is often the easiest "no-code" UI approach, but it requires them to have a NordVPN account. It keeps the traffic entirely off the public internet.

### 3\. Rootless Podman Network Mapping

Because you use **Rootless Podman** (UID 1000), your containers are already naturally isolated from the root system.

*   **How it works:** We can change how the container "talks" to the host. Instead of the container listening on all interfaces, we can bind it specifically to a virtual bridge that only the SSH tunnel can see.
*   **The "Wall":** This adds a second layer of protection. Even if your firewall (firewalld) had a leak, the container literally wouldn't be "listening" for anyone except the authenticated tunnel user.

* * *

### Comparison for GreyServer

| Feature | SSH Tunnel (Restricted) | NordVPN Meshnet |
| --- | --- | --- |
| **Security** | Highest (Granular port control) | High (Encrypted P2P) |
| **Setup** | Host-side config changes | App-based invites |
| **User Experience** | Needs a terminal command | "Just works" once invited |

**Which of these directions feels like the best fit for your colleague's technical level?**

* * *

### 📑 Manifest Update Block (Conceptual)

```
## 3. Networking & Security (Planned)
* **Access Model:** Evaluating Restricted SSH Tunnel vs. Meshnet Peer-to-Peer.
* **Goal:** Zero-knowledge access to application ports (3100/8080) for external peers.
```

## Prompt:
No Meshnet it will be by IP Only and the container need to be able to register data on the external drive but I do not want the user to be able to access any of my server.sevices via SSH except the container

## Response:
Home Server assistant said
--------------------------

Since you want to stick to a direct **IP-based SSH tunnel** and ensure the container can still write to your external drive (`/mnt/GreyServer/data/`), we have a clear path. This setup respects your **Disaster Recovery (DRP)** principle by keeping the "Host" (OS) and "Disk" (Data) distinct while strictly isolating the user.

Here are the possible solutions to achieve this without code:

### 1\. The "Restricted Tunnel" User (Recommended)

You create a unique system user on your Fedora host specifically for your colleague.

*   **The Restriction:** You configure SSH so that when this specific user connects, the server "locks" them into a tunnel-only mode.
*   **The Result:** They can use their SSH client to map the container's port (like 8080 or 3100) to their own machine, but if they try to type a command or see your other services (like Cockpit on 9090), the connection simply does nothing or closes.
*   **Data Integrity:** Because the container itself is already configured via `podman-compose` to mount folders from `/mnt/GreyServer/data/`, the colleague can interact with the app, and the app will save data to your drive, but the colleague never "sees" the drive directly.

### 2\. SSH "PermitOpen" White-listing

This is a more surgical version of the first option.

*   **The Restriction:** You tell the SSH daemon that this specific user is _only_ allowed to touch one internal IP/Port combination.
*   **The Result:** Even if they knew the port for your AI service or your system logs, the SSH "gatekeeper" would block those requests before they even reach the container engine.
*   **Security:** This is the strongest way to ensure they don't poke around your local LAN (`192.168.1.0/24`).

### 3\. Dedicated Container Network Bridge

Currently, your containers likely sit on a default bridge. We can move the specific container they need to its own "isolated" virtual network.

*   **The Restriction:** The container lives in a private "room" that doesn't talk to the other containers (like Homebox or YouTrack).
*   **The Result:** Even if your colleague somehow bypassed the SSH restriction (which is unlikely), they would find themselves in a network with only one destination available.
*   **Storage Safety:** This doesn't change how the container writes to `/mnt/GreyServer/data/`, so your persistence remains intact.

### Why this works for GreyServer:

*   **Rootless Podman:** Since you run as User 1000, these guest tunnels don't have root privileges on your host.
*   **SELinux:** Your existing labels (`svirt_sandbox_file_t`) will continue to protect the rest of your drive from the container, even while your colleague is using it.

**Would you like me to explain how we would verify the "PermitOpen" restriction to ensure your other ports (like 9090) are invisible to them?**

* * *

### 📑 Manifest Update Block (Architectural)

```
## 3. Networking & Security (Proposed)
* **External Collaboration:** IP-based SSH Tunneling via restricted guest account.
* **Access Control:** "PermitOpen" logic to isolate specific container ports.
* **Storage Policy:** Container-level volume mounts to /mnt/GreyServer/data/ (User 1000).
```

## Prompt:
It's ok, I guess solution 3 will be the best if needed. I will keep the chat - and try to do do if needed, in which case I will come back to you

## Response:
Home Server assistant said
--------------------------

That sounds like a solid plan. Using a **Dedicated Container Network Bridge** (Solution 3) is the cleanest architectural choice for **GreyServer**. It aligns perfectly with your goal of keeping the "Host" (Fedora 43) and "Disk" (`/mnt/GreyServer/`) isolated while allowing the container to process data locally.

By placing that specific container on its own virtual network, you ensure that even if a guest is tunneled into that port, they are effectively "trapped" in a single room with no visibility into your other services like **Homebox** or **YouTrack**. Your **SELinux** policies and **Rootless Podman** setup will continue to act as the primary guards for your physical hardware.

I've updated the internal tracking of your setup. Whenever you're ready to implement this, just let me know.

* * *

### 📑 Manifest Update Block (Archived)

```
## 4. Service Inventory (Networking Note)
* **Future Provision:** Isolated Bridge Network ('guest-link') identified for external peer access.
* **Security constraint:** No cross-container communication between 'guest-link' and 'default' podman network.
* **Storage:** Continues to use UID 1000 mapping to /mnt/GreyServer/data/ for persistence.
```

**Would you like me to summarize the specific Podman commands you'll need to create that isolated bridge when the time comes?**

## Prompt:
hum, when thinking about it, maybe the user will need to have restrictred access to the data on one subfolder on disc ... eg mounting galaxy container for testing implementation of a dashboard, so he might need access to some part

## Response:
Home Server assistant said
--------------------------

That changes the architectural requirement slightly, but **GreyServer's** rootless Podman setup actually handles this very well. Since your host and disk are distinct, we can "slice" a piece of your storage specifically for that container.

### The Solution: Targeted Volume Mapping

Instead of giving the user access to your filesystem, you give the **container** access to a specific subfolder, and the user accesses that folder _through_ the container's dashboard or interface.

*   **Subfolder Isolation**: You can create a specific path, for example, `/mnt/GreyServer/data/galaxy-test/`, and map only that folder to the container.
*   **Permissions**: Because you use **Rootless Podman (UID 1000)**, the container will only have the same permissions you do; it cannot "break out" to see your backups or other service configs.
*   **SELinux Protection**: By using the `:Z` or `:z` flag during the mount (or via your existing `semanage` labels), Fedora 43 will ensure the container is cryptographically locked to that specific folder.

### How the User Interacts

1.  **The User**: Connects via the restricted SSH tunnel you mentioned earlier.
2.  **The Container**: Runs the dashboard (like Galaxy) and looks at the mapped subfolder.
3.  **The Interaction**: The user uploads or edits files _inside_ the dashboard. The container then writes those files directly to `/mnt/GreyServer/data/galaxy-test/`.

**Result**: Your colleague gets to test the dashboard and manipulate data, but they never actually "touch" your command line or your drive directly. Everything happens inside the "box."

* * *

### 📑 Manifest Update Block (Revision)

```
## 2. Storage & Filesystem (Addendum)
* **Guest Testing:** Targeted mount at `/mnt/GreyServer/data/galaxy-test/`.
* **Security:** SELinux `svirt_sandbox_file_t` enforced.
* **Access Path:** User -> SSH Tunnel -> Container Port -> Dashboard -> Local Storage.
```

**Would you like me to outline how to set the specific SELinux permissions for that new subfolder so the container doesn't run into "Permission Denied" errors?**



---
Powered by [Gemini Exporter](https://www.ai-chat-exporter.com)
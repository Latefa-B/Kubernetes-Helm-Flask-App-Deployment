# Kubernetes Package Management with Helm
Kubernetes is an open-source platform for automating deployment, scaling, and management of containerized applications. It introduces the Pod as the smallest deployable unit. The Pod encapsulates one or more containers that share the same network, namespace and can access shared storage volumes. This abstraction allows Kubernetes to manage groups of tightly coupled containers as a single logical unit, simplifying communication and coordination. Kubernetes as an orchestration tool for containers, allows them to run reliably, scale up and down, and communicate with each other across many servers, making sure the application is always running and has enough resources.

Previously, we demonstrated how to deploy applications to Kubernetes using raw YAML files. While YAML is powerful for defining individual Kubernetes resources (Pods, Deployments, Services, etc.), managing complex applications that consist of many inter-related resources for a single application can quickly become cumbersome, specially when you need to configure them differently for development, staging, and production environments ! To address this, Helm comes as a solution. Often called "the package manager for Kubernetes." We can consider Helm Charts like apt packages or npm packages, but for Kubernetes applications. It allows you to :
- Package Kubernetes applications into reusable units called Charts.
- Define configurable values for your applications, making it easy to deploy the same application with different settings across environments.
- Manage the lifecycle of your Kubernetes applications (install, upgrade, rollback, delete) as a single unit.

This comprehensive step-by-step guide walks you through the process of deploying an application using Kubernetes Package Management with Helm. In this project, we will learn the basics of Helm by packaging our Flask application into a Helm Chart and deploying it. The aim of this project is to learn :  
- The purpose and benefits of Helm for Kubernetes application management.
- The structure of a Helm Chart.
- How to create a basic Helm Chart for our Flask application.
- How to define configurable values in values.yaml.
- How to use Helm commands (helm install, helm upgrade, helm uninstall).
- How to deploy an application using a Helm Chart.

## Prerequisites
- Have understood Deployments, Services, and ConfigMaps/Secrets.
- Have Helm Installed: Follow the official Helm installation guide for your operating system (Search for "Install Helm").
<img width="969" height="45" alt="0" src="https://github.com/user-attachments/assets/f682f29c-77b5-4f2d-afd0-fb59769be0be" />

- Have Minikube installed and running on your computer.
- The my-config-app Docker image built locally.
<img width="569" height="131" alt="0" src="https://github.com/user-attachments/assets/d3c8f484-4370-47a8-81eb-cf992e6b459c" />


## Step-by-step instructions

### Step 1: Create a Basic Helm Chart
A Helm Chart is a collection of files that describe a related set of Kubernetes resources. When you initialize a new Helm Chart, it creates a standard directory structure with template files and a values.yaml file. To complete Step 1 follow the instructions below : 
- Open your command line or terminal and Navigate to your kubernetes-labs folder.
- Create a new Helm Chart named my-flask-chart using the command : helm create my-flask-chart 
**Expected output** : This command creates a new directory my-flask-chart with a default structure. You will see files like Chart.yaml, values.yaml, and a templates folder.

- Explore the generated chart structure using the command :  ls -R my-flask-chart
<img width="864" height="214" alt="2" src="https://github.com/user-attachments/assets/9eac1c4c-b349-4462-b979-f9139c1cda7e" />

**Expected output** : Your structure should look like this : 

**Chart.yaml**: Contains metadata about the chart (name, version, description).
**values.yaml**: Contains the default configuration values for the chart.
templates/**: Contains the actual Kubernetes YAML manifest files, but with templating logic.
charts/**: Can contain other Helm Charts (dependencies).
<img width="487" height="272" alt="3" src="https://github.com/user-attachments/assets/d2deab43-60b4-4196-9504-7873fe1644ea" />

### Step 2: Customize Your Helm Chart for the Flask App
We'll modify the default deployment.yaml and service.yaml templates to match our Flask application. We'll also update values.yaml to define configurable parameters like the Docker image, replica count, and service type. To complete Step 2 follow the instructions below : 
- Delete unnecessary default files using the commands : rm my-flask-chart/templates/hpa.yaml && rm my-flask-chart/templates/ingress.yaml && rm my-flask-chart/templates/serviceaccount.yaml
**Note** : We will keep deployment.yaml, service.yaml, NOTES.txt, and _helpers.tpl.
<img width="705" height="42" alt="4" src="https://github.com/user-attachments/assets/8a0d5134-ef69-499c-bc2d-e7f196465678" />


- Update the following yaml files : values.yaml, deployment.yaml and service.yaml.
- Open my-flask-chart/values.yaml and replace its content with:
<img width="640" height="438" alt="4" src="https://github.com/user-attachments/assets/f391807e-617c-4831-82d3-783622d7b823" />

- Open my-flask-chart/templates/deployment.yaml and replace its content with:
<img width="947" height="888" alt="5" src="https://github.com/user-attachments/assets/c2ed26e1-785c-46b8-a936-09aa7486e3ba" />


- Open my-flask-chart/templates/service.yaml and replace its content with:
<img width="647" height="291" alt="6" src="https://github.com/user-attachments/assets/3bfbf019-c685-4470-acea-6dec552c13ad" />

**Note**: _helpers.tpl contains reusable templates for labels and names, which we leverage here.

### Step 3: Package and Install Your Helm Chart
Once your Chart is defined, you can install it into your Kubernetes cluster. Helm will take your templates and values.yaml, render the final Kubernetes YAML manifests, and then apply them to the cluster. To complete Step 3 follow the instructions below : 
- Ensure your Minikube cluster is running using the command : minikube start
<img width="1416" height="210" alt="1" src="https://github.com/user-attachments/assets/6c5e9ee0-7f34-4fad-b9e5-cbe293abcfaf" />

- Open your command line or terminal and Navigate to your kubernetes-labs folder.
- Lint your chart and check for errors using the command : helm lint my-flask-chart 

**Expected output** : You should see 0 warnings and 0 errors.
<img width="1454" height="149" alt="7" src="https://github.com/user-attachments/assets/debe85a7-4822-4673-8ac5-aaf5f88ee6d8" />


**Error** : [ERROR] templates/: … nil pointer evaluating interface {}.enabled.  1 chart (s) linted, 1 chart (s) failed.
**Explanation** : This error means that httpRoute, autoscaling, ingress and service account values are not defined in the values.yaml file. Helm is trying to access them on a nil (null) object. When you write Helm charts, the templates often include conditional logic, Helm templates expect certain keys in values.yaml file.

**Solution** : Define the missing value in values.yaml and set up Helm to use the default service account. 

**Troubleshooting steps** : 
- Step 1 : Add the following values to httpRoute, autoscaling, serviceAccount and ingress in your values.yaml file.
<img width="620" height="590" alt="8" src="https://github.com/user-attachments/assets/05d3c0da-af82-4c9c-877d-40c3af7f7fb8" />


- Step 2 : lint your flask chart using the command : helm lint my-flask-chart
<img width="626" height="105" alt="9" src="https://github.com/user-attachments/assets/4ac22d7e-43c2-4117-bdaa-34288581dc61" />

- Install your chart using the command : helm install my-flask-app-release my-flask-chart
<img width="1357" height="197" alt="10" src="https://github.com/user-attachments/assets/61a712dc-cbc7-46e7-bd45-06f25e759694" />


- Here is the command breakdown :
**helm install** : The command to install a chart.
**my-flask-app-release : This is the release name. Helm uses this to manage your installation. It must be unique within a namespace.
**my-flask-chart** : The path to your chart folder.
**Expected output** : You should see output indicating the release was deployed, along with helpful notes (from NOTES.txt).
- Verify Kubernetes resources created by Helm using the command : kubectl get all -l app.kubernetes.io/instance=my-flask-app-release 

**Expected output** : You should see a Deployment, ReplicaSet, and Pod (or Pods if you set replicaCount higher) and a Service, all named with my-flask-app-release-my-flask-chart.

<img width="788" height="150" alt="11" src="https://github.com/user-attachments/assets/c7a1f5df-88fa-40de-ba45-3dae23b14e8e" />


- Check Helm release status using the command : helm list
**Expected output** : You should see my-flask-app-release listed with STATUS: deployed.
<img width="1053" height="89" alt="12" src="https://github.com/user-attachments/assets/06296657-b57a-4059-80e5-347270b56c3c" />


### Step 4: Access Your Helm-Deployed Application
Just like with our manual deployments, we need to access our application. Since we used a ClusterIP Service, we'll use minikube service for easy access. To complete Step 4 follow the instructions below : 
- Access your application using the command : minikube service my-flask-app-release-my-flask-chart --url
- Copy the URL and paste it into your web browser.
<img width="1219" height="64" alt="13" src="https://github.com/user-attachments/assets/e08232ab-2c11-4252-a47c-158f2ae2f654" />

**Error** : the service my-flask-app-release-my-flask-chart has a ClusterIP service type, not meant to be exposed. 

**Explanation** :  the command minikube service <service-name> --url only works for services of type NodePort or LoadBalancer, not with services of type ClusterIP.
**Solution** : Alternatively, we will access our Application using kubectl port-forward to the Service or switch the service to service type NodePort or LoadBalancer. In this case, I will be using Port-forward.

**Troubleshooting steps** : 
- Step 1 : If you are running your cluster from an AWS EC2 instance, make sure to configure your workstation security groups and to allow inbound rules on port 5000 and your VPC’s NACL . to allow inbound rules on port 5000
- Go to EC2 Dashboard → Instances → your EC2 Instance → security → security groups → Inbound rules → Edit inbound rules → add rule to allow custom TCP traffic on port 5000 → save rules.
<img width="1453" height="642" alt="14" src="https://github.com/user-attachments/assets/fbd27018-5fef-4959-ac73-1f68c6c946c8" />

- Go to VPC Dashboard → Network ACLs → select your Network ACLs → Edit inbound rules → add new rule → Define settings (Type : Custom TCP, Protocol : TCP, Port : 5000, Source : 0.0.0.0/0) → save rules. 
<img width="1437" height="689" alt="15" src="https://github.com/user-attachments/assets/0e593b23-0c53-4ab9-b621-2dfacdb92c2c" />


- Go to VPC Dashboard → Network ACLs → select your Network ACLs → Edit outbound rules → add new rule → Define settings (Type : Custom TCP, Protocol : TCP, Port : 1024-65535, Source : 0.0.0.0/0) → save rules. 
<img width="1443" height="621" alt="16" src="https://github.com/user-attachments/assets/775e4c4f-68c3-4546-8e46-926fa03bd365" />

- Step 2 : Run Port-forward command to forward traffic from 8080 to port 5000 on my-flask-app-release-my-flask-chart service.
- Open a new terminal window, run : kubectl port-forward –address 0.0.0.0 service/my-flask-app-release-my-flask-chart 8080:5000. This forwards traffic from local port 8080 to port 5000 on the x-service.
<img width="966" height="226" alt="22" src="https://github.com/user-attachments/assets/4b4bb55b-0594-47e1-9338-b4f3f451433b" />


- Step 3 : Access your flask application locally (Optional)
- Run on your terminal the command : curl http://127.0.0.1:8080 or curl http://localhost:8080 to check the application locally.
<img width="886" height="886" alt="23" src="https://github.com/user-attachments/assets/9f39e3ae-d0d5-49c0-981a-c8774db099b4" />
<img width="871" height="247" alt="24" src="https://github.com/user-attachments/assets/9b0c4cfb-88bd-49ea-9b6b-43f1a11f36f9" />


- Step 4 : Access your flask application from the Web Browser
- Type on your web browser : http://<ec2-public-ip>:5000 to reach the application.
**Expected output** : You should see your "Config & Secret App" with the message "Hello from Helm! This is a configurable message." This confirms Helm successfully injected the values from values.yaml.
<img width="854" height="682" alt="26" src="https://github.com/user-attachments/assets/08c26a08-6288-4bbc-95db-49cf7896a41e" />


### Step 5: Upgrade Your Helm Release
One of Helm's biggest advantages is easy upgrades. You can change values in values.yaml or update your templates, then use helm upgrade to apply the changes. Helm will perform a rolling update of your application. To complete Step 5 follow the instructions below : 
- Edit my-flask-chart/values.yaml: Change the env.APP_CONFIG_MESSAGE to a new value:
- Save my-flask-chart/values.yaml.
<img width="631" height="609" alt="27" src="https://github.com/user-attachments/assets/58e51c18-e8bd-4516-b467-11a0a8cf4bff" />

- Upgrade your Helm release using the command : helm upgrade my-flask-app-release my-flask-chart
**Expected output** : You should see output indicating a successful upgrade.
<img width="1346" height="215" alt="28" src="https://github.com/user-attachments/assets/c0199ff4-c85f-46ac-98d5-cf699728a1c6" />

- Watch the rolling update using the command : kubectl get pods -l app.kubernetes.io/instance=my-flask-app-release -w 

**Expected output** : You will see the old Pod terminating and a new one spinning up.
<img width="868" height="75" alt="29" src="https://github.com/user-attachments/assets/96dd42c3-725d-4cb0-90c0-5a1f03b615ff" />

- Verify the updated message : Refresh your web browser at the minikube service URL from Step 4.

**Expected output** : You should now see the new message: "Helm upgrade successful! New message here."
<img width="920" height="684" alt="30" src="https://github.com/user-attachments/assets/af23e9b4-6708-48b5-af03-633875d30dfe" />



### Step 6 : Clean Up (Optional but Recommended)
To completely remove your Helm release and all the Kubernetes resources it created, you use helm uninstall. To complete Step 6 follow the instructions below : 
- Uninstall your Helm release using the command : helm uninstall my-flask-app-release 
**Expected output** : You should see output indicating the release was uninstalled.

- Verify resources are gone using the command : kubectl get all -l app.kubernetes.io/instance=my-flask-app-release
**Expected output** : Should show "No resources found..."

<img width="898" height="83" alt="31" src="https://github.com/user-attachments/assets/b9dca2c2-4cd0-4204-8a69-e27901a73332" />


- Stop Minikube cluster using the command : minikube stop 
<img width="599" height="71" alt="32" src="https://github.com/user-attachments/assets/4b224b7e-b11d-4c72-985e-5276930abdf4" />

### Summary 
This breakdown provides a step-by-step guide to deploy  an Application using Kubernetes Package Management with Helm. By completing this project, we had an overview on : 
- How to create a basic Helm Chart for our Flask application.
- How to define configurable values in values.yaml.
- How to use Helm commands (helm install, helm upgrade, helm uninstall).
- How to deploy an application using a Helm Chart.

By deploying the application in this lab, we gained hands-on experience with Helm, Kubernetes’ powerful package manager. We demonstrated how Helm simplifies the deployment and management of complex applications within a kubernetes cluster. By using Helm charts, we were able to package, configure, and deploy the application in a repeatable and consistent manner. 

Throughout the project, we installed Helm, added chart repositories, deployed applications, and customized their configurations using values.yaml files. This process showcased Helm’s ability to streamline Kubernetes operations, reduce human error, and support efficient CI/CD workflows in cloud-native environments. But also, reinforced the importance of Helm as a key tool in Kubernetes package management, enabling scalable and maintainable application deployments.

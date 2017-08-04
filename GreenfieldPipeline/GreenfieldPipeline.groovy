env.APPDYNAMIC_VERSION="4.2.7_+"
env.nexusRepository="http://maven-repo.tvlport.com:8082/nexus/content/repositories"

def getRegions(){
    def ADC2a8fde4 = [REGION_NAME: 'adc', CLUSTER_NAME: '2a8fde4', CLUSTER: 'api.adc-2a8fde4-gf.travelport.com', DOMAIN: 'adc-gf.travelport.com']
    def ADC3a9fde5 = [REGION_NAME: 'adc', CLUSTER_NAME: '3a9fde5', CLUSTER: 'api.adc-3a9fde5-gf.travelport.com', DOMAIN: 'adc-gf.travelport.com']
    def ZU29vb2qdz = [REGION_NAME: 'zu2', CLUSTER_NAME: '9vb2qdz', CLUSTER: 'api.zu2-9vb2qdz-gf.travelport.com', DOMAIN: 'zu2-gf.travelport.com']
    def ZEW7d4nwzp = [REGION_NAME: 'zew', CLUSTER_NAME: '7d4nwzp', CLUSTER: 'api.zew-7d4nwzp-gf.travelport.com', DOMAIN: 'zew-gf.travelport.com']
    def ZASudhr3p6 = [REGION_NAME: 'zas', CLUSTER_NAME: 'udhr3p6', CLUSTER: 'api.zas-udhr3p6-gf.travelport.com', DOMAIN: 'zas-gf.travelport.com']
    def Regions = [ADC2a8fde4, ADC3a9fde5, ZU29vb2qdz, ZEW7d4nwzp, ZASudhr3p6]
    return Regions
}

def getRegion(Region_Name)
{
    def Regions = getRegions()
    def myRegion = []
    for(currentRegion in Regions){
        if(currentRegion.REGION_NAME == Region_Name){
            myRegion.add(currentRegion)
        }
    }
    return myRegion
}

def getCluster(Cluster_Name)
{
    def Regions = getRegions()
    def myCluster = []
    for(currentRegion in Regions){
        if(currentRegion.CLUSTER_NAME == Cluster_Name){
            myCluster.add(currentRegion)
            break;
        }
    }
    return myCluster
}

def getNonProdRegions(){
    def ADCDVr3yc172 = [REGION_NAME: 'adc-dv', CLUSTER_NAME: 'r3yc172', CLUSTER: 'api.adc-dv-r3yc172-gf.travelport.com', DOMAIN: 'adc-dv-gf.travelport.com']
    def ZU2DV4d3vapi = [REGION_NAME: 'zu2-dv', CLUSTER_NAME: '4d3vapi', CLUSTER: 'api.zu2-dv-4d3vapi-gf.travelport.com', DOMAIN: 'zu2-dv-gf.travelport.com']
    def ZEWDV4d3vapi = [REGION_NAME: 'zew-dv', CLUSTER_NAME: '4d3vapi', CLUSTER: 'api.zew-dv-4d3vapi-gf.travelport.com', DOMAIN: 'zew-dv-gf.travelport.com']
    def ZASDV4d3vapi = [REGION_NAME: 'zas-dv', CLUSTER_NAME: '4d3vapi', CLUSTER: 'api.zas-dv-4d3vapi-gf.travelport.com', DOMAIN: 'zas-dv-gf.travelport.com']
    def Regions = [ADCDVr3yc172, ZU2DV4d3vapi, ZEWDV4d3vapi, ZASDV4d3vapi]
    return Regions
}

def getNonProdRegion(){
    def ADCDVr3yc172 = [REGION_NAME: 'adc-dv', CLUSTER_NAME: 'r3yc172', CLUSTER: 'api.adc-dv-r3yc172-gf.travelport.com', DOMAIN: 'adc-dv-gf.travelport.com']
    return ADCDVr3yc172
}

def getNonProdRegion(Region_Name)
{
    def Regions = getNonProdRegions()
    def myRegion = []
    for(currentRegion in Regions){
        if(currentRegion.REGION_NAME == Region_Name){
            myRegion.add(currentRegion)
        }
    }
    return myRegion
}

def getNonProdCluster(Region_Name, Cluster_Name)
{
    def Regions = getNonProdRegion(Region_Name)
    def myCluster = []
    for(currentRegion in Regions){
        if(currentRegion.CLUSTER_NAME == Cluster_Name){
            myCluster.add(currentRegion)
            break;
        }
    }
    return myCluster
}

def git_checkout(giturl){
    git_checkout giturl, '*/master', true
}

def git_checkout(giturl, gitbranch){
    git_checkout giturl, gitbranch, true
}

def git_checkout(giturl, gitbranch, clean){
    if(clean == true){
        step([$class: 'WsCleanup'])
    }
    sh "rm -f .gitconfig.lock"
    sh "git config --global http.sslVerify 'false'"
    checkout([$class: 'GitSCM', branches: [[name: gitbranch]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'CleanBeforeCheckout']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'fc9bed0b-4af9-49c3-ab29-d4a78f346b2e', url: giturl]]])
}

def git_checkout_tag(giturl, gittag, clean){
    if(clean == true){
        step([$class: 'WsCleanup'])
    }
    def refName = "refs/tags/${gittag}"
    sh "rm -f .gitconfig.lock"
    sh "git config --global http.sslVerify 'false'"
    checkout([$class: 'GitSCM', branches: [[name: refName]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'CleanBeforeCheckout']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'fc9bed0b-4af9-49c3-ab29-d4a78f346b2e', url: giturl]]])
}

def checkdocs(docUrl){
    String libUrl = docUrl.replace(" ","%20")
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'abb94883-fb49-48f1-b834-4b0f1e48317e', usernameVariable: 'SP_USERNAME', passwordVariable: 'SP_PASSWORD']]) {
        sh "curl --ntlm --fail --user '${env.SP_USERNAME}':'${env.SP_PASSWORD}' '${libUrl}' > /dev/null" 
    }
}

def sonar(){
   sh "mvn -s settings.xml sonar:sonar"
}
 
def sonar(pomfile){
   sh "mvn -s settings.xml -f $pomfile sonar:sonar"
}
 
def sonar_clean(){
   sh "mvn -s settings.xml clean compile sonar:sonar"
}

def sonar_clean_pom(pomfile){
   sh "mvn -s settings.xml -f $pomfile clean compile sonar:sonar"
}
 
def fortify_scan(){
    sh "mvn -s settings.xml sca:clean sca:translate sca:scan"
}
 
def fortify_scan(pomfile){
    sh "mvn -s settings.xml -f $pomfile sca:clean sca:translate sca:scan"
}

def fortify_scan_clean(){
    sh "mvn -s settings.xml clean compile sca:clean sca:translate sca:scan"
}

def fortify_scan_clean_pom(pomfile){
    sh "mvn -s settings.xml -f $pomfile clean compile sca:clean sca:translate sca:scan"
}

def appdynamics_setup(){
	try {
		stackato "create-service user-provided appdynamics --credentials host-name:travelportms.saas.appdynamics.com --credentials port:443 --credentials password:'' --credentials host:travelportms.saas.appdynamics.com --credentials account-access-key:1e5e4cd82c55 --credentials account-name:travelportms --credentials ssl-enabled:true  --credentials appdynamics.http.proxyHost:pn-outbound-proxy.tvlport.com --credentials appdynamics.http.proxyPort:30375"
	} catch (Exception e) {}
    return env.APPDYNAMIC_VERSION
}

// Next Generation of AppD Setups - based on application name and only creates the AppD environment they want sicne appname is unique in CF
def appdynamics_setup(appDSvcName, environmentKey){
	try {
		if(environmentKey == "DV"){
			stackato "create-service user-provided appdynamics_${appDSvcName} --credentials host-name:travelportms.saas.appdynamics.com --credentials port:443 --credentials password:'' --credentials host:travelportms.saas.appdynamics.com --credentials account-access-key:1e5e4cd82c55 --credentials account-name:travelportms --credentials ssl-enabled:true --credentials appdynamics.http.proxyHost:pn-outbound-proxy.tvlport.com --credentials appdynamics.http.proxyPort:30375"
		}else if (environmentKey == "PF") {
			stackato "create-service user-provided appdynamics_${appDSvcName} --credentials host-name:travelportpf.saas.appdynamics.com --credentials port:443 --credentials password:'' --credentials host:travelportpf.saas.appdynamics.com --credentials account-access-key:p3sybeblzkv8 --credentials account-name:travelportpf --credentials ssl-enabled:true --credentials appdynamics.http.proxyHost:pn-outbound-proxy.tvlport.com --credentials appdynamics.http.proxyPort:30375"
		}else if (environmentKey == "PP") {
		stackato "create-service user-provided appdynamics_${appDSvcName} --credentials host-name:travelportpp.saas.appdynamics.com --credentials port:443 --credentials password:'' --credentials host:travelportpp.saas.appdynamics.com --credentials account-access-key:4db8eb08201e --credentials account-name:travelportpp --credentials ssl-enabled:true --credentials appdynamics.http.proxyHost:pn-outbound-proxy.tvlport.com --credentials appdynamics.http.proxyPort:30375"
		}else if (environmentKey == "PN") {
		stackato "create-service user-provided appdynamics_${appDSvcName} --credentials host-name:travelport.saas.appdynamics.com --credentials port:443 --credentials password:'' --credentials host:travelport.saas.appdynamics.com --credentials account-access-key:ae9243e80451 --credentials account-name:travelport --credentials ssl-enabled:true --credentials appdynamics.http.proxyHost:pn-outbound-proxy.tvlport.com --credentials appdynamics.http.proxyPort:30375"
		}else if (environmentKey == "AZURE_PN") {
		stackato "create-service user-provided appdynamics_${appDSvcName} --credentials host-name:travelport.saas.appdynamics.com --credentials port:443 --credentials password:'' --credentials host:travelport.saas.appdynamics.com --credentials account-access-key:ae9243e80451 --credentials account-name:travelport --credentials ssl-enabled:true"
		}
	} catch (Exception e) {}
	return env.APPDYNAMIC_VERSION
}

def appdynamics_remove(appDSvcName){
	try {
		stackato "delete-service --no-prompt --unbind appdynamics_${appDSvcName}"
	} catch (Exception e) {}
}

def appdynamics_config(appDSvcName){
    appdynamics_config (appDSvcName, appDSvcName, env.APPDYNAMIC_VERSION)
}

def appdynamics_config(appDSvcName, appDName){
	appdynamics_config (appDSvcName, appDName, env.APPDYNAMIC_VERSION)
}

def appdynamics_config(svcName, appDName, appDVersion){
	try {
        stackato "env-add ${svcName} JBP_CONFIG_APP_DYNAMICS_AGENT '[ repository_root: \"https://java-buildpack.cloudfoundry.org/app-dynamics\", default_application_name: ${appDName}, version: ${appDVersion} ]' "		
        stackato "env-add ${svcName} JBP_CONFIG_COMPONENTS \"{ frameworks: [ 'JavaBuildpack::Framework::AppDynamicsAgent', 'JavaBuildpack::Framework::ContainerCertificateTrustStore', 'JavaBuildpack::Framework::ContainerCustomizer', 'JavaBuildpack::Framework::Debug', 'JavaBuildpack::Framework::DynatraceAppmonAgent', 'JavaBuildpack::Framework::DynatraceOneAgent', 'JavaBuildpack::Framework::Jmx', 'JavaBuildpack::Framework::JrebelAgent', 'JavaBuildpack::Framework::LunaSecurityProvider', 'JavaBuildpack::Framework::MariaDbJDBC', 'JavaBuildpack::Framework::NewRelicAgent', 'JavaBuildpack::Framework::PlayFrameworkAutoReconfiguration', 'JavaBuildpack::Framework::PlayFrameworkJPAPlugin', 'JavaBuildpack::Framework::PostgresqlJDBC', 'JavaBuildpack::Framework::SpringAutoReconfiguration', 'JavaBuildpack::Framework::SpringInsight', 'JavaBuildpack::Framework::YourKitProfiler', 'JavaBuildpack::Framework::JavaOpts' ] } \" "
     } catch (Exception e) {}
}

def dvproxy_setup(){
	try {
		stackato "create-service user-provided dv-outbound-proxy --credentials hostname:dv-outbound-proxy.tvlport.com --credentials host:dv-outbound-proxy.tvlport.com --credentials port:30375 --credentials password:''"
    } catch (Exception e) {}
}

def atlproxy_setup(){
	try {
		stackato "create-service user-provided atlproxy --credentials host:atlproxy.tvlport.com --credentials port:8080"
    } catch (Exception e) {}
}

def getDVFrameworkVIPs(){
    def DVZookeeperVip1 = [VIP_NAME: 'ZookeeperVip1-config', FRAMEWORK_VIP: 'zk1-gf-dv.travelport.com' ]
    def DVZookeeperVip2 = [VIP_NAME: 'ZookeeperVip2-config', FRAMEWORK_VIP: 'zk2-gf-dv.travelport.com']
    def DVFrameworkVIPs = [DVZookeeperVip1, DVZookeeperVip2]
    return DVFrameworkVIPs
}

def getFrameworkVIPs(){
    def ZookeeperVip1 = [VIP_NAME: 'ZookeeperVip1-config', FRAMEWORK_VIP: 'zk1-gf.travelport.com']
    def ZookeeperVip2 = [VIP_NAME: 'ZookeeperVip2-config', FRAMEWORK_VIP: 'zk2-gf.travelport.com']
    def ZookeeperVip3 = [VIP_NAME: 'ZookeeperVip3-config', FRAMEWORK_VIP: 'zk3-gf.travelport.com']
    def FrameworkVIPs = [ZookeeperVip1, ZookeeperVip2, ZookeeperVip3]
    return FrameworkVIPs
}

def Restframework_nonprod_setup(){
    def VIPs = getDVFrameworkVIPs()
    for(currentVIP in VIPs){ 
        try{
            stackato "create-service user-provided $currentVIP.VIP_NAME --credentials host:$currentVIP.FRAMEWORK_VIP --credentials port:'2281' --credentials password:'' --credentials com.travelport.odt.ssl.truststore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.ssl.keystore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.restfw.zookeeper:zk1-gf-dv.travelport.com:2281,zk2-gf-dv.travelport.com:2281"    
        } catch (Exception e) {}
        try{
            stackato "update-user-provided-service $currentVIP.VIP_NAME --credentials host:$currentVIP.FRAMEWORK_VIP --credentials port:'2281' --credentials password:'' --credentials com.travelport.odt.ssl.truststore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.ssl.keystore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.restfw.zookeeper:zk1-gf-dv.travelport.com:2281,zk2-gf-dv.travelport.com:2281"    
        } catch (Exception e) {}
    }
}

def Resframework_setup(){
    def VIPs = getFrameworkVIPs()
    for(currentVIP in VIPs){ 
        try{
            stackato "create-service user-provided $currentVIP.VIP_NAME --credentials host:$currentVIP.FRAMEWORK_VIP --credentials port:'2281' --credentials password:'' --credentials com.travelport.odt.ssl.truststore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.ssl.keystore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.restfw.zookeeper:zk1-gf.travelport.com:2281,zk2-gf.travelport.com:2281,zk3-gf.travelport.com:2281"    
        } catch (Exception e) {}
        try{
            stackato "update-user-provided-service $currentVIP.VIP_NAME --credentials host:$currentVIP.FRAMEWORK_VIP --credentials port:'2281' --credentials password:'' --credentials com.travelport.odt.ssl.truststore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.ssl.keystore.phrase:VHJhdmVscG9ydDFTdG9yZVBhc3M= --credentials com.travelport.odt.restfw.zookeeper:zk1-gf.travelport.com:2281,zk2-gf.travelport.com:2281,zk3-gf.travelport.com:2281"    
        } catch (Exception e) {}
    }
}

def Restframework_nonprod_bind(serviceName){
    def VIPs = getDVFrameworkVIPs()
    for(currentVIP in VIPs){ 
        try{
            stackato "bind-service $currentVIP.VIP_NAME ${serviceName}"
        } catch (Exception e) {}
    }
}

def Restframework_bind(serviceName){
    def VIPs = getFrameworkVIPs()
    for(currentVIP in VIPs){ 
        try{
            stackato "bind-service $currentVIP.VIP_NAME ${serviceName}"
        } catch (Exception e) {}
    }
}   

def config_repo_nonprod_setup(){
	try {
		stackato "create-service user-provided config-repo --credentials host:vhldvrmut001.tvlport.net --credentials port:37051 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:vhldvrmut001.tvlport.net:37051"
		//stackato "create-service user-provided config-repo002 --credentials host:VHLPNELLL002.tvlport.net --credentials port:33651 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo003 --credentials host:VHLPNELLL003.tvlport.net --credentials port:33652 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo004 --credentials host:VHLPNELLL004.tvlport.net --credentials port:33653 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo005 --credentials host:VHLPNELLL005.tvlport.net --credentials port:33654 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo006 --credentials host:VHLPNELLL006.tvlport.net --credentials port:33655 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo007 --credentials host:VHLPNELLL007.tvlport.net --credentials port:33656 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo008 --credentials host:VHLPNELLL008.tvlport.net --credentials port:33657 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
	} catch (Exception e) {}
}

def config_repo_prod_setup(){
	try {
		stackato "create-service user-provided config-repo --credentials host:VHLPNELLL001.tvlport.net --credentials port:33650 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650"
		//stackato "create-service user-provided config-repo002 --credentials host:VHLPNELLL002.tvlport.net --credentials port:33651 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo003 --credentials host:VHLPNELLL003.tvlport.net --credentials port:33652 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo004 --credentials host:VHLPNELLL004.tvlport.net --credentials port:33653 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo005 --credentials host:VHLPNELLL005.tvlport.net --credentials port:33654 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo006 --credentials host:VHLPNELLL006.tvlport.net --credentials port:33655 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo007 --credentials host:VHLPNELLL007.tvlport.net --credentials port:33656 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
		//stackato "create-service user-provided config-repo008 --credentials host:VHLPNELLL008.tvlport.net --credentials port:33657 --credentials password:'' --credentials com.travelport.odt.restfw.zookeeper:VHLPNELLL001.tvlport.net:33650,VHLPNELLL002.tvlport.net:33651,VHLPNELLL003.tvlport.net:33652,VHLPNELLL004.tvlport.net:33653,VHLPNELLL005.tvlport.net:33654,VHLPNELLL006.tvlport.net:33655,VHLPNELLL007.tvlport.net:33656,VHLPNELLL008.tvlport.net:33657"
	} catch (Exception e) {}
}

def dynatrace_setup(){
	try {
		stackato "create-service user-provided dynatrace --credentials server:10.4.125.29:9998 --credentials host:10.4.125.29 --credentials port:9998"
    } catch (Exception e) {}
}

def stackato(command){
	try {
		sh "stackato ${command}"
    } catch (Exception e) {}
}

def stackato_ex(command){
	sh "stackato ${command}"
}

def stackato_login(org, space){
    stackato_login "https://api.adc-dv-r3yc172-gf.travelport.com", org, space
}

def stackato_login(url, org, space){
    env.https_proxy="https://atlproxy.tvlport.com:8080/"
    def credentialID = "f9f3f09d-f275-45f9-bca9-7376435a8098"
    compareUrl = url.replace("https://","")
    if(compareUrl.equals("api.adc-dv-r3yc172-gf.travelport.com")){
        switch(org) {
            case "InfraSvcOrg": 
                credentialID = "823c6ed8-b422-42d7-aa05-650158c3d742"
                break
            case "AirCommOrg":
                credentialID = "78b0cd66-9353-48a8-a41e-c23bafb38373"
                break
            case "COEOrg":
                credentialID = "fc68f0dc-a91b-47d4-afb3-7bb1a2022717"
                break
            case "HospitalityOrg":
                credentialID = "372386b8-2aa1-4a5e-94f9-a13697c6853a"
                break
            case "PlatSvcOrg":
                credentialID = "9668de75-6f4e-4bf9-ac54-2fe40751452b"
                break
            default:
                credentialID = "f9f3f09d-f275-45f9-bca9-7376435a8098"
                break
        }
    }

    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: credentialID, usernameVariable: 'CF_USERNAME', passwordVariable: 'CF_PASSWORD']]) {
		def logInSuccess = false
        def validated = false
		def attemptCount = 0
		def maxAttempts = 10
		
		while(!logInSuccess) {   
			try {
				attemptCount++
				println 'Login attempt # ' + attemptCount
				stackato_ex "login '${env.CF_USERNAME}' --password '${env.CF_PASSWORD}' --target ${url} --organization ${org} --space ${space}"
				println 'Login Success at attempt # ' + attemptCount
				logInSuccess=true
	        } catch (Exception e){ 
				println 'Failed to Login - retrying shortly...'
				sleep(2)
				if(attemptCount>10){
					break
				}
			}
    	}
		
		if(!logInSuccess) { 
			throw new Exception('Unable to Log Into Stackato - Load Corrupted')
		}
		println 'Outside Login Process'
		stackato "target ${url} --organization ${org} --space ${space}"

        //def userID = "NOT IDENTIFIED"
        //try {
        //    wrap([$class: 'BuildUser']) {
        //        def users = sh(returnStdout: true, script: "stackato org-users ${org}").split("\r?\n")
        //        for(line in users){   
        //            if(line.contains("${BUILD_USER_ID}")){
        //                validated = true
        //                break
        //            }
        //        }
        //        userID = BUILD_USER_ID
        //    }
        //} catch (Exception e) {
        //    println "User: ${userID} Let it pass for now"
        //}
        // Temporary If for NonProd
        //if(compareUrl.equals("api.adc-dv-r3yc172-gf.travelport.com")){
        //    if(!validated && !userID.equals("NOT IDENTIFIED")) {
        //        stackato_logout()
        //        errorString = "${userID} is not a member of ${org}"
        //        throw new Exception(errorString)
        //    }
        //}
        
	}
}


def stackato_logout(){
	try {
		stackato "logout"
    } catch (Exception e) {}
}

def archive_build(giturl){
    archive_build giturl, 'master'
}

def archive_build(giturl, gitbranch){
    archive_build giturl, gitbranch, ''
}

def archive_build(giturl, gitbranch, appName){
    def path = "archive"
    // if(gitbranch.equals("master")){
    //    path = "archive/${appName}"
    // }
    sh "mkdir -p ${path}"
    sh "curl -k --output ${path}/console-${appName}.log --user svcjenkinsjobs:d3f2797fa06eecb5e9625531a4abefb2 ${BUILD_URL}consoleText"

    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'fc9bed0b-4af9-49c3-ab29-d4a78f346b2e', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        String secureUrl = giturl.replace("https://","@")
        sh "git config user.email ${GIT_USERNAME}"
        sh "git config user.name ${GIT_USERNAME}"

        sh "git add ${path}/*"
        sh "git commit ${path}/* -m 'Console Logged'"
     	sh "git push https://'${GIT_USERNAME}':'${GIT_PASSWORD}'${secureUrl} HEAD:${gitbranch}"
    }

}

def tag_build(giturl, gitbranch){
    pom = readMavenPom file: 'pom.xml'
    def version = "v$pom.version"
    tag_build(giturl, gitbranch, version)
}

def tag_build(giturl, gitbranch, mytag){
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'fc9bed0b-4af9-49c3-ab29-d4a78f346b2e', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        String secureUrl = giturl.replace("https://","@")
        sh "git config user.email ${GIT_USERNAME}"
        sh "git config user.name ${GIT_USERNAME}"
        sh "git tag $mytag"
        sh "git push https://'${GIT_USERNAME}':'${GIT_PASSWORD}'${secureUrl} HEAD:${gitbranch} --tag"
    }    
}

def get_release(){
    pom = readMavenPom file: 'pom.xml'
    get_release(env.nexusRepository, pom.groupId, pom.artifactId, pom.version)
    return pom.version
}

def get_release(pomFile){
    pom = readMavenPom file: pomFile
    get_release(env.nexusRepository, pom.groupId, pom.artifactId, pom.version)
    return pom.version
}

def get_release(groupId, artifactId, version){
    get_release(env.nexusRepository, groupId, artifactId, version)
}

def get_release(repoUrl, groupId, artifactId, version){
    env.http_proxy="http://atlproxy.tvlport.com:8080/"
    sh "mkdir -p target"
    wrap([$class: 'ConfigFileBuildWrapper', managedFiles: [[fileId: 'org.jenkinsci.plugins.configfiles.maven.MavenSettingsConfig1448996998298', targetLocation: 'settings.xml', variable: '']]]) {
        sh "mvn -s settings.xml org.apache.maven.plugins:maven-dependency-plugin:2.8:copy -DrepoUrl=${env.nexusRepository} -Dartifact=${groupId}:${artifactId}:${version}:war -DoutputDirectory=target -Dmdep.stripVersion=true"
    }
}

def get_version(){
    pom = readMavenPom file: 'pom.xml'
    return pom.version
}

def archive_md5(giturl, gitbranch){
    pom = 'pom.xml'
    archive_md5(giturl, gitbranch, pom, env.nexusRepository)
}

def archive_md5(giturl, gitbranch, pomFile, repoURL){
    def path = "archive"
    
    sh "mkdir -p ${path}"
    sh "rm -f ${path}/*.md5"
    get_md5(repoURL, pomFile)
    sh "cp *.md5 ${path}/."

    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'fc9bed0b-4af9-49c3-ab29-d4a78f346b2e', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        String secureUrl = giturl.replace("https://","@")
        sh "git config user.email ${GIT_USERNAME}"
        sh "git config user.name ${GIT_USERNAME}"

        sh "git add ${path}/*.md5"
        sh "git commit ${path}/*.md5 -m 'md5 saved'"
     	sh "git push https://'${GIT_USERNAME}':'${GIT_PASSWORD}'${secureUrl} HEAD:${gitbranch}"
    }

}

def confirm_md5(){
    pom = 'pom.xml'
    confirm_md5(env.nexusRepository, pom)
}

def confirm_md5(pomFile){
    confirm_md5(env.nexusRepository, pomFile)
}

def confirm_md5(repoUrl, pomFile){
    get_md5(repoUrl, pomFile)
    def archive = sh(returnStdout: true, script: "ls archive/*.md5").trim()
    def current = sh(returnStdout: true, script: "ls *.md5").trim()
    def archiveMD5 = sh(returnStdout: true, script: "tail ${archive}").trim()
    def currentMD5 = sh(returnStdout: true, script: "tail ${current}").trim()
    if(archiveMD5.equals(currentMD5)){
        println "MD5 Confirmed"
        return "true"
    } else {
        println "FAILED MD5 Check"
        return "false"
    }
}

def get_md5(){
    pom = 'pom.xml'
    get_md5(env.nexusRepository, pom)
}

def get_md5(pomFile){
    get_md5(env.nexusRepository, pomFile)
}

def get_md5(repoUrl, pomFile){
    env.http_proxy="http://atlproxy.tvlport.com:8080/"
    pom = readMavenPom file: pomFile
    def groupId = pom.groupId.replace(".","/")
    def md5Url = "${repoUrl}/releases/${groupId}/${pom.artifactId}/${pom.version}/${pom.artifactId}-${pom.version}.war.md5"
    sh "curl -k --output ${pom.artifactId}-${pom.version}.war.md5 ${md5Url}"
}

def get_running_app(route, url, org, space){
   stackato_login(url, org, space)
   return get_running_app(route)
}

def get_running_app(url){
    def trimedUrl = url.replace("https://","")
    def searchUrl = trimedUrl.toLowerCase()
    def routes = sh(returnStdout: true, script: "stackato routes").split("\r?\n")
    for(line in routes){   
        if(line.contains("${searchUrl}")){
            def columns = line.tokenize("|")
            return columns[2].trim()
        }
    }
    return "None"
}

def publish_alert_nonprod(alertFile){
    sh "cp ${alertFile} /mnt/jenkins/tools/elastalert/elastalert_rules/nonprod/."    
}
 
def publish_alert_prod(alertFile){
    sh "cp ${alertFile} /mnt/jenkins/tools/elastalert/elastalert_rules/prod/."    
}

def git_clone_akana_scripts() {
    try{
        sh "git clone -b master https://gitbucket.tvlport.com/git/GREENFIELD/GreenfieldAdmin.git"
    } catch (Exception e) {}
}

def createApi() {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
        try{
            sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python createApi.py"
        } catch (Exception e) {}
    }
}

def createNewApiVersion() {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
        try{
            sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python createNewApiVersion.py"
        } catch (Exception e) {}
    }
}

def attachPolicies() {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
        try{
            sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python attachPolicies.py"
        } catch (Exception e) {}
    }
}

def addDoc() {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
        try{
            sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python addDoc.py"
        } catch (Exception e) {}
    }
}

def deleteApi() {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
        try{
            sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python deleteApi.py"
        } catch (Exception e) {}
    }
}

def deleteApiVersion() {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
        try{
            sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python deleteApiVersion.py"
        } catch (Exception e) {}
    }
}

def upload_toc(giturl, gitbranch, projectName, buildName) {
    def path = "/var/jenkins_home/workspace/" + projectName + "/" + buildName + "/apidocs"

    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'fc9bed0b-4af9-49c3-ab29-d4a78f346b2e', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        String secureUrl = giturl.replace("https://","@")
        sh "git config user.email ${GIT_USERNAME}"
        sh "git config user.name ${GIT_USERNAME}"

        sh "git add " + path + "/*"
        sh "git commit ${path}/* -m 'toc file uploaded to git repo'"
        sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}${secureUrl} HEAD:${gitbranch}"
    }
}

// def addToc() {
//     withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
//         try{
//             sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python addToc.py"
//         } catch (Exception e) {}
//     }
// }

// def addDoc() {
//     withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: '9e7471c8-f994-4a64-b670-12ee5f90803a', usernameVariable: 'Akanauser', passwordVariable: 'Akanapass']]){
//         try{
//             sh "cd GreenfieldAdmin/GreenfieldPipeline/akana_scripts; python addDoc.py"
//         } catch (Exception e) {}
//     }
// }

return this;

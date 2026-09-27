plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "sg.edwingarage.readonlybridge"
    compileSdk = 35
    defaultConfig {
        applicationId = "sg.edwingarage.readonlybridge"
        minSdk = 26
        targetSdk = 35
        versionCode = 7
        versionName = "2.2.0"
    }
    buildTypes { release { isMinifyEnabled = false } }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

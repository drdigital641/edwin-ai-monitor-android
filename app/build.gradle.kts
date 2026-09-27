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
        versionCode = 4
        versionName = "1.2-same-bubble-time"
    }
    buildTypes { release { isMinifyEnabled = false } }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

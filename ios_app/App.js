import React, { useState } from 'react';
import { 
  StyleSheet, 
  View, 
  SafeAreaView,
  StatusBar,
  ActivityIndicator,
  Alert
} from 'react-native';
import { WebView } from 'react-native-webview';

export default function App() {
  const [loading, setLoading] = useState(true);
  
  // ضع رابط البوت هنا بعد نشره
  const BOT_URL = 'https://your-bot-url.repl.co'; // غيّر هذا الرابط!
  
  // إذا البوت مو منشور، استخدم رابط localhost للتجربة:
  // const BOT_URL = 'http://192.168.8.139:5000';

  const handleLoadStart = () => setLoading(true);
  const handleLoadEnd = () => setLoading(false);
  
  const handleError = (error) => {
    Alert.alert(
      'خطأ في الاتصال',
      'تأكد من اتصال الإنترنت ومن أن البوت يعمل',
      [{ text: 'حسناً' }]
    );
    setLoading(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#667eea" />
      
      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#667eea" />
        </View>
      )}
      
      <WebView
        source={{ uri: BOT_URL }}
        style={styles.webview}
        onLoadStart={handleLoadStart}
        onLoadEnd={handleLoadEnd}
        onError={handleError}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={true}
        scalesPageToFit={true}
        bounces={false}
        allowsBackForwardNavigationGestures={true}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#667eea',
  },
  webview: {
    flex: 1,
  },
  loadingContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
    zIndex: 1,
  },
});

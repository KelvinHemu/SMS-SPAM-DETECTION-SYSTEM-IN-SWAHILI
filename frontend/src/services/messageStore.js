/**
 * Real-time Message Store
 * Handles communication between sender and receiver devices
 */

class MessageStore {
  constructor() {
    // Add instance tracking
    this.instanceId = Math.random().toString(36).substr(2, 9);
    console.log('🏗️ MessageStore: Creating new instance', this.instanceId);
    
    this.messages = [];
    this.listeners = [];
    this.deliveryStats = {
      total: 0,
      delivered: 0,
      blocked: 0
    };
    this.subscriptionId = 0; // Add subscription tracking
  }

  // Add listener for real-time updates
  subscribe(listener) {
    this.subscriptionId++;
    const currentId = this.subscriptionId;
    console.log('➕ MessageStore: [' + this.instanceId + '] Adding subscription #' + currentId, 'Total listeners will be:', this.listeners.length + 1);
    
    this.listeners.push(listener);
    
    return () => {
      console.log('➖ MessageStore: [' + this.instanceId + '] Removing subscription #' + currentId, 'Total listeners will be:', this.listeners.length - 1);
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  // Notify all listeners of changes
  notify() {
    console.log('🔔 MessageStore: [' + this.instanceId + '] Broadcasting to', this.listeners.length, 'active listeners');
    console.log('📋 MessageStore: [' + this.instanceId + '] Current messages:', this.messages.map(m => ({
      id: m.id, 
      text: m.text.substring(0, 15) + '...', 
      sender: m.senderPhone,
      receiver: m.receiverPhone,
      delivered: m.isDelivered
    })));
    
    this.listeners.forEach((listener, index) => {
      try {
        console.log('📤 MessageStore: [' + this.instanceId + '] Notifying listener #' + (index + 1));
        listener(this.messages);
      } catch (error) {
        console.error('❌ MessageStore: [' + this.instanceId + '] Error notifying listener #' + (index + 1), error);
      }
    });
  }

  // Add message from sender with immediate delivery to receiver
  async addMessage(senderPhone, receiverPhone, messageText, analysisResult) {
    console.log('🏪 MessageStore: [' + this.instanceId + '] Adding new message:', {
      senderPhone,
      receiverPhone,
      messageText: messageText.substring(0, 20) + '...',
      decision: analysisResult.decision,
      isDelivered: analysisResult.delivery_result?.status === 'delivered',
      isBlocked: analysisResult.decision === 'BLOCKED'
    });
    
    const message = {
      id: Date.now(),
      text: messageText,
      senderPhone,
      receiverPhone,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      analysisResult,
      // Extract key info from analysis
      decision: analysisResult.decision,
      confidence: analysisResult.confidence,
      isDelivered: analysisResult.delivery_result?.status === 'delivered',
      isBlocked: analysisResult.decision === 'BLOCKED',
      spamLabel: this.getSpamLabel(analysisResult)
    };

    this.messages.push(message);
    console.log('🏪 MessageStore: [' + this.instanceId + '] Total messages now:', this.messages.length);
    
    // Also store in window for debugging
    if (typeof window !== 'undefined') {
      window.messageStoreDebug = {
        instanceId: this.instanceId,
        messages: this.messages,
        listeners: this.listeners.length
      };
    }
    
    this.updateStats(message);
    
    // Notify all components immediately
    console.log('🔔 MessageStore: [' + this.instanceId + '] About to notify listeners...');
    this.notify();
    console.log('✅ MessageStore: [' + this.instanceId + '] Notification complete');
    
    return message;
  }

  // Generate spam detection label for display
  getSpamLabel(analysisResult) {
    const { decision, confidence } = analysisResult;
    
    switch (decision) {
      case 'CLEAN':
        return null; // No label needed for clean messages
      case 'CONTENT_WARNING':
        return {
          type: 'warning',
          text: `⚠️ Content Warning (${Math.round(confidence * 100)}% confidence)`,
          color: 'bg-yellow-100 text-yellow-800 border-yellow-200'
        };
      case 'SENDER_WARNING':
        return {
          type: 'sender',
          text: `🚨 Sender Warning (${Math.round(confidence * 100)}% confidence)`,
          color: 'bg-orange-100 text-orange-800 border-orange-200'
        };
      case 'BLOCKED':
        return {
          type: 'blocked',
          text: `🚫 Message Blocked - Spam Detected (${Math.round(confidence * 100)}% confidence)`,
          color: 'bg-red-100 text-red-800 border-red-200'
        };
      default:
        return null;
    }
  }

  // Get messages for specific receiver
  getMessagesForReceiver(receiverPhone) {
    console.log('🔍 MessageStore: [' + this.instanceId + '] Filtering messages for receiver:', receiverPhone);
    console.log('🔍 MessageStore: [' + this.instanceId + '] All messages:', this.messages.map(m => ({
      id: m.id,
      sender: m.senderPhone,
      receiver: m.receiverPhone,
      delivered: m.isDelivered,
      blocked: m.isBlocked,
      text: m.text.substring(0, 20) + '...'
    })));
    
    const filtered = this.messages.filter(msg => {
      const match = msg.receiverPhone === receiverPhone && msg.isDelivered && !msg.isBlocked;
      console.log('🔍 Checking message:', {
        id: msg.id,
        receiverMatch: msg.receiverPhone === receiverPhone,
        isDelivered: msg.isDelivered,
        isNotBlocked: !msg.isBlocked,
        finalMatch: match
      });
      return match;
    });
    
    console.log('🔍 MessageStore: [' + this.instanceId + '] Filtered messages:', filtered.length);
    return filtered;
  }

  // Get messages from specific sender
  getMessagesFromSender(senderPhone) {
    return this.messages.filter(msg => msg.senderPhone === senderPhone);
  }

  // Update delivery statistics
  updateStats(message) {
    this.deliveryStats.total++;
    if (message.isDelivered) {
      this.deliveryStats.delivered++;
    }
    if (message.isBlocked) {
      this.deliveryStats.blocked++;
    }
  }

  // Get delivery statistics
  getStats() {
    return {
      ...this.deliveryStats,
      successRate: this.deliveryStats.total > 0 
        ? Math.round((this.deliveryStats.delivered / this.deliveryStats.total) * 100)
        : 0
    };
  }

  // Clear all messages (for testing)
  clear() {
    this.messages = [];
    this.deliveryStats = { total: 0, delivered: 0, blocked: 0 };
    this.notify();
  }

  // Test method to verify store is working
  test() {
    console.log('🧪 MessageStore Test: [' + this.instanceId + '] Store is accessible');
    console.log('🧪 Current messages:', this.messages.length);
    console.log('🧪 Current listeners:', this.listeners.length);
    console.log('🧪 Detailed messages:', this.messages);
    return {
      instanceId: this.instanceId,
      messagesCount: this.messages.length,
      listenersCount: this.listeners.length,
      isWorking: true,
      messages: this.messages
    };
  }
}

// Ensure global singleton - use window object as backup
let messageStoreInstance;

if (typeof window !== 'undefined') {
  // Browser environment
  if (!window.__messageStore) {
    console.log('🌐 Creating global messageStore instance on window');
    window.__messageStore = new MessageStore();
  } else {
    console.log('🌐 Using existing global messageStore instance from window');
  }
  messageStoreInstance = window.__messageStore;
} else {
  // Node environment (shouldn't happen in frontend)
  messageStoreInstance = new MessageStore();
}

// Export the singleton instance
export const messageStore = messageStoreInstance;
export default messageStoreInstance; 
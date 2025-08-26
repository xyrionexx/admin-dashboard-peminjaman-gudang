<div class="space-y-6">
  <div class="flex items-center justify-between">
    <h1 class="text-3xl font-bold text-gray-900">Settings</h1>
  </div>
  
  <!-- Settings Sections -->
  <div class="space-y-6">
    <!-- General Settings -->
    <div class="bg-white rounded-lg shadow-sm border">
      <div class="p-6 border-b">
        <h2 class="text-lg font-semibold text-gray-900">General Settings</h2>
      </div>
      <div class="p-6 space-y-4">
        <div>
          <label for="siteName" class="block text-sm font-medium text-gray-700 mb-2">Site Name</label>
          <input id="siteName" type="text" value="AdminPro Dashboard" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
        </div>
        <div>
          <label for="siteDescription" class="block text-sm font-medium text-gray-700 mb-2">Site Description</label>
          <textarea id="siteDescription" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">Modern admin dashboard for managing your business</textarea>
        </div>
      </div>
    </div>
    
    <!-- Notification Settings -->
    <div class="bg-white rounded-lg shadow-sm border">
      <div class="p-6 border-b">
        <h2 class="text-lg font-semibold text-gray-900">Notifications</h2>
      </div>
      <div class="p-6 space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-gray-900">Email Notifications</p>
            <p class="text-sm text-gray-600">Receive email updates about your account</p>
          </div>
          <input type="checkbox" checked class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" aria-labelledby="emailNotifications" />
        </div>
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-gray-900">Push Notifications</p>
            <p class="text-sm text-gray-600">Receive push notifications in your browser</p>
          </div>
          <input type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" aria-labelledby="pushNotifications" />
        </div>
      </div>
    </div>
  </div>
  
  <div class="flex justify-end">
    <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
      Save Changes
    </button>
  </div>
</div>

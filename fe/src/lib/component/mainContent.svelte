<script>
	const stats = [
		{ title: 'Total Users', value: '12,345', change: '+12%', color: 'text-green-600' },
		{ title: 'Revenue', value: '$45,678', change: '+8%', color: 'text-green-600' },
		{ title: 'Orders', value: '1,234', change: '-3%', color: 'text-red-600' },
		{ title: 'Products', value: '567', change: '+15%', color: 'text-green-600' }
	];
</script>

<main class="flex-1 overflow-y-auto p-6">
	<!-- Header -->
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
		<p class="text-gray-600 mt-2">
			Welcome back! Here's what's happening with your business today.
		</p>
	</div>

	<!-- Stats Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
		{#each stats as stat}
			<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-sm font-medium text-gray-600">{stat.title}</p>
						<p class="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
					</div>
					<div class="text-right">
						<span class={`text-sm font-medium ${stat.color}`}>{stat.change}</span>
						<p class="text-xs text-gray-500 mt-1">vs last month</p>
					</div>
				</div>
			</div>
		{/each}
	</div>

	<!-- Content Cards -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
		<!-- Recent Activity -->
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
			<h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
			<div class="space-y-4">
				{#each Array(5) as _, i}
					<div class="flex items-center space-x-3">
						<div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
							<svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
								<path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
								<path
									fill-rule="evenodd"
									d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
									clip-rule="evenodd"
								></path>
							</svg>
						</div>
						<div class="flex-1">
							<p class="text-sm font-medium text-gray-900">New user registered</p>
							<p class="text-xs text-gray-500">{5 - i} minutes ago</p>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<!-- Quick Actions -->
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
			<h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
			<div class="grid grid-cols-2 gap-4">
				<button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
					<svg
						class="w-8 h-8 text-blue-600 mx-auto mb-2"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 6v6m0 0v6m0-6h6m-6 0H6"
						></path>
					</svg>
					<p class="text-sm font-medium text-gray-900">Add User</p>
				</button>
				<button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
					<svg
						class="w-8 h-8 text-green-600 mx-auto mb-2"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
						></path>
					</svg>
					<p class="text-sm font-medium text-gray-900">New Product</p>
				</button>
				<button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
					<svg
						class="w-8 h-8 text-purple-600 mx-auto mb-2"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
						></path>
					</svg>
					<p class="text-sm font-medium text-gray-900">Generate Report</p>
				</button>
				<button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
					<svg
						class="w-8 h-8 text-orange-600 mx-auto mb-2"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z"
						></path>
					</svg>
					<p class="text-sm font-medium text-gray-900">Settings</p>
				</button>
			</div>
		</div>
	</div>
</main>

<script lang="ts">
	interface StatCard {
		title: string;
		value: string;
		icon: string;
		bgColor: string;
		iconColor: string;
	}

	interface ActivityItem {
		message: string;
		time: string;
		status: 'success' | 'info' | 'warning';
	}

	const stats: StatCard[] = [
		{
			title: 'Total Users',
			value: '12,345',
			icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z',
			bgColor: 'bg-blue-100',
			iconColor: 'text-blue-600'
		},
		{
			title: 'Revenue',
			value: '$45,678',
			icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1',
			bgColor: 'bg-green-100',
			iconColor: 'text-green-600'
		},
		{
			title: 'Orders',
			value: '1,234',
			icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
			bgColor: 'bg-yellow-100',
			iconColor: 'text-yellow-600'
		},
		{
			title: 'Growth',
			value: '+23%',
			icon: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6',
			bgColor: 'bg-purple-100',
			iconColor: 'text-purple-600'
		}
	];

	const recentActivity: ActivityItem[] = [
		{ message: 'New user registered: john@example.com', time: '2 minutes ago', status: 'success' },
		{ message: 'Order #1234 completed', time: '5 minutes ago', status: 'info' },
		{ message: 'Payment pending for order #1235', time: '10 minutes ago', status: 'warning' }
	];

	function getStatusColor(status: ActivityItem['status']): string {
		switch (status) {
			case 'success':
				return 'bg-green-500';
			case 'info':
				return 'bg-blue-500';
			case 'warning':
				return 'bg-yellow-500';
			default:
				return 'bg-gray-500';
		}
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
		<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
			Add New
		</button>
	</div>

	<!-- Stats Cards -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		{#each stats as stat}
			<div class="bg-white p-6 rounded-lg shadow-sm border">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-sm text-gray-600">{stat.title}</p>
						<p class="text-2xl font-bold text-gray-900">{stat.value}</p>
					</div>
					<div class="p-3 {stat.bgColor} rounded-full">
						<svg
							class="w-6 h-6 {stat.iconColor}"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={stat.icon}
							></path>
						</svg>
					</div>
				</div>
			</div>
		{/each}
	</div>

	<!-- Recent Activity -->
	<div class="bg-white rounded-lg shadow-sm border">
		<div class="p-6 border-b">
			<h2 class="text-lg font-semibold text-gray-900">Recent Activity</h2>
		</div>
		<div class="p-6">
			<div class="space-y-4">
				{#each recentActivity as activity}
					<div class="flex items-center space-x-4">
						<div class="w-2 h-2 {getStatusColor(activity.status)} rounded-full"></div>
						<p class="text-sm text-gray-600">{activity.message}</p>
						<span class="text-xs text-gray-400">{activity.time}</span>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>

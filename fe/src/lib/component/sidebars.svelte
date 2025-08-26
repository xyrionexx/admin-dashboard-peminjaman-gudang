<script lang="ts">
	import logo from '../../lib/assets/logo.png';
	interface NavigationItem {
		name: string;
		icon: string;
		active?: boolean;
	}

	interface Props {
		collapsed: boolean;
		mobileOpen: boolean;
		activePage: string;
		onToggle: () => void;
		onCloseMobile: () => void;
		onPageChange: (pageName: string) => void;
	}

	interface Props {
		collapsed: boolean;
		mobileOpen: boolean;
		activePage: string;
		onToggle: () => void;
		onCloseMobile: () => void;
		onPageChange: (pageName: string) => void;
	}

	let { collapsed, mobileOpen, activePage, onToggle, onCloseMobile, onPageChange }: Props =
		$props();

	const navigationItems: NavigationItem[] = [
		{
			name: 'Dashboard',
			icon: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z',
			active: true
		},
		{
			name: 'Analytics',
			icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
		},
		{
			name: 'Users',
			icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z'
		},
		{ name: 'Products', icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4' },
		{
			name: 'Barang',
			icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'
		},
		{
			name: 'Reports',
			icon: 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
		},
		{
			name: 'Settings',
			icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'
		}
	];
</script>

<aside
	class={`
  ${mobileOpen ? 'translate-x-0' : '-translate-x-full'} 
  fixed 
  inset-y-0 left-0 
  z-50 lg:static lg:translate-x-0 
  ${collapsed ? 'w-16' : 'w-64'} 
  flex flex-col border-r border-gray-200 
  bg-white shadow-lg transition-all
  duration-300 ease-in-out
`}
>
	<!-- Header -->
	<div class="flex items-center justify-between border-b border-gray-200 p-4">
		{#if !collapsed}
			<div class="flex items-center space-x-2">
				<div class="flex h-8 w-8 items-center justify-center rounded-lg p-1">
					<i><img src={logo} alt="" /></i>
				</div>
				<span class="text-xl font-bold text-gray-800">G-Ware</span>
			</div>
		{/if}

		<!-- Desktop toggle button -->
		<button
			onclick={onToggle}
			class="hidden rounded-md p-1.5 text-gray-500 transition-colors hover:bg-gray-100 lg:flex"
			aria-label="Toggle Sidebar"
		>
			<svg
				class={`h-4 w-4 transition-transform ${collapsed ? 'rotate-180' : ''}`}
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
			>
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"
				></path>
			</svg>
		</button>

		<!-- Mobile close button -->
		<button
			onclick={onCloseMobile}
			class="rounded-md p-1.5 text-gray-500 hover:bg-gray-100 lg:hidden"
			aria-label="Close Sidebar"
		>
			<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M6 18L18 6M6 6l12 12"
				></path>
			</svg>
		</button>
	</div>

	<!-- Navigation -->
	<nav class="flex-1 space-y-2 overflow-y-auto px-4 py-6">
		{#each navigationItems as item}
			<button
				type="button"
				onclick={() => onPageChange(item.name)}
				class={`
          flex w-full items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-colors
          ${
						activePage === item.name
							? 'border-r-2 border-blue-700 bg-blue-50 text-blue-700'
							: 'text-gray-700 hover:bg-gray-100'
					}
          ${collapsed ? 'justify-center' : 'space-x-3'}
        `}
				aria-label={item.name}
			>
				<svg class="h-5 w-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={item.icon}
					></path>
				</svg>
				{#if !collapsed}
					<span>{item.name}</span>
				{/if}
			</button>
		{/each}
	</nav>

	<!-- User Profile -->
	<div class="border-t border-gray-200 p-4">
		<div class={`flex items-center ${collapsed ? 'justify-center' : 'space-x-3'}`}>
			<img
				src="/placeholder.svg?height=40&width=40"
				alt="Admin Avatar"
				class="h-10 w-10 rounded-full"
			/>
			{#if !collapsed}
				<div class="min-w-0 flex-1">
					<p class="truncate text-sm font-medium text-gray-900">Admin User</p>
					<p class="truncate text-xs text-gray-500">admin@company.com</p>
				</div>
				<button class="rounded-md p-1 text-gray-400 hover:text-gray-600" aria-label="User Settings">
					<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
						></path>
					</svg>
				</button>
			{/if}
		</div>
	</div>
</aside>

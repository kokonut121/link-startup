'use client'

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Bell, Bookmark, BriefcaseIcon, HomeIcon, MessageCircle, UserIcon, Search } from "lucide-react"
import { useToast } from "@/components/ui/use-toast"

type Opportunity = {
  id: number
  title: string
  company: string
  description: string
  tags: string[]
  type: string
  location: string
  salary: number
  experience: string
  saved: boolean
  applied: boolean
}

type Filters = {
  types: string[]
  locations: string[]
  experience: string
  remote: boolean
}

const initialOpportunities: Opportunity[] = [
  {
    id: 1,
    title: "Software Engineering Intern",
    company: "TechCorp",
    description: "TechCorp is looking for passionate students to join our summer internship program...",
    tags: ["React", "Node.js", "AWS"],
    type: "Internship",
    location: "San Francisco, CA",
    salary: 25,
    experience: "Entry Level",
    saved: false,
    applied: false,
  },
  {
    id: 2,
    title: "Data Science Intern",
    company: "DataCo",
    description: "Join DataCo for an exciting internship in the field of data science and machine learning...",
    tags: ["Python", "Machine Learning", "SQL"],
    type: "Internship",
    location: "New York, NY",
    salary: 22,
    experience: "Entry Level",
    saved: false,
    applied: false,
  },
  {
    id: 3,
    title: "UX Design Intern",
    company: "DesignHub",
    description: "DesignHub is seeking creative minds for our UX design internship program...",
    tags: ["Figma", "User Research", "Prototyping"],
    type: "Internship",
    location: "Remote",
    salary: 20,
    experience: "Entry Level",
    saved: false,
    applied: false,
  },
]

export default function HomePage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>(initialOpportunities)
  const [activeTab, setActiveTab] = useState("recent")
  const [searchTerm, setSearchTerm] = useState("")
  const [filters, setFilters] = useState<Filters>({
    types: [],
    locations: [],
    experience: "",
    remote: false,
  })
  const { toast } = useToast()

  const handleSave = (id: number) => {
    setOpportunities(opportunities.map(opp => 
      opp.id === id ? { ...opp, saved: !opp.saved } : opp
    ))
    toast({
      title: "Opportunity Saved",
      description: "The opportunity has been added to your saved list.",
    })
  }

  const handleApply = (id: number) => {
    setOpportunities(opportunities.map(opp => 
      opp.id === id ? { ...opp, applied: true } : opp
    ))
    toast({
      title: "Application Submitted",
      description: "Your application has been successfully submitted.",
    })
  }

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value)
  }

  const handleFilterChange = (filterType: keyof Filters, value: Filters[keyof Filters]) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }))
  }

  const filteredOpportunities = opportunities.filter(opp => 
    (opp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    opp.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    opp.description.toLowerCase().includes(searchTerm.toLowerCase())) &&
    (filters.types.length === 0 || filters.types.includes(opp.type)) &&
    (filters.locations.length === 0 || filters.locations.includes(opp.location)) &&
    (filters.experience === "" || filters.experience === opp.experience) &&
    (!filters.remote || opp.location === "Remote")
  )

  const displayedOpportunities = activeTab === "saved" 
    ? filteredOpportunities.filter(opp => opp.saved)
    : activeTab === "applied"
    ? filteredOpportunities.filter(opp => opp.applied)
    : filteredOpportunities

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left Sidebar */}
      <aside className="w-64 bg-white shadow-lg p-6 hidden md:block">
        <div className="text-2xl font-bold text-purple-700 mb-8">StudentConnect</div>
        <nav className="space-y-4">
          <Link href="#" className="flex items-center space-x-3 text-gray-700 hover:text-purple-700 transition-colors duration-200">
            <HomeIcon className="h-5 w-5" />
            <span>Home</span>
          </Link>
          <Link href="#" className="flex items-center space-x-3 text-gray-700 hover:text-purple-700 transition-colors duration-200">
            <BriefcaseIcon className="h-5 w-5" />
            <span>Opportunities</span>
          </Link>
          <Link href="#" className="flex items-center space-x-3 text-gray-700 hover:text-purple-700 transition-colors duration-200">
            <MessageCircle className="h-5 w-5" />
            <span>Messages</span>
          </Link>
          <Link href="#" className="flex items-center space-x-3 text-gray-700 hover:text-purple-700 transition-colors duration-200">
            <UserIcon className="h-5 w-5" />
            <span>Profile</span>
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        {/* Header */}
        <header className="bg-white shadow-sm sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
            <div className="relative w-64">
              <Input 
                className="pl-10 text-black placeholder-gray-500 border-gray-300" 
                placeholder="Search opportunities..." 
                value={searchTerm}
                onChange={handleSearch}
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="icon" className="text-purple-700 hover:text-purple-900 hover:bg-purple-100">
                <Bell className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="text-purple-700 hover:text-purple-900 hover:bg-purple-100">
                <MessageCircle className="h-5 w-5" />
              </Button>
              <Avatar>
                <AvatarImage src="./placeholder.svg?height=32&width=32" alt="@username" />
                <AvatarFallback>UN</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </header>

        {/* Filters */}
        <div className="bg-white shadow-sm mt-4 p-6 rounded-lg mx-4">
          <div className="max-w-7xl mx-auto space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                <Select
                  value={filters.types.join(',')}
                  onValueChange={(value) => handleFilterChange('types', value.split(',').filter(Boolean))}
                >
                  <SelectTrigger className="w-full border-gray-300 text-black">
                    <SelectValue placeholder="Select types" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Internship">Internship</SelectItem>
                    <SelectItem value="Full-time">Full-time</SelectItem>
                    <SelectItem value="Part-time">Part-time</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                <Select
                  value={filters.locations.join(',')}
                  onValueChange={(value) => handleFilterChange('locations', value.split(',').filter(Boolean))}
                >
                  <SelectTrigger className="w-full border-gray-300 text-black">
                    <SelectValue placeholder="Select locations" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="San Francisco, CA">San Francisco, CA</SelectItem>
                    <SelectItem value="New York, NY">New York, NY</SelectItem>
                    <SelectItem value="Austin, TX">Austin, TX</SelectItem>
                    <SelectItem value="Chicago, IL">Chicago, IL</SelectItem>
                    <SelectItem value="Remote">Remote</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Experience</label>
                <Select
                  value={filters.experience}
                  onValueChange={(value) => handleFilterChange('experience', value)}
                >
                  <SelectTrigger className="w-full border-gray-300 text-black">
                    <SelectValue placeholder="Select experience" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Entry Level">Entry Level</SelectItem>
                    <SelectItem value="1-2 years">1-2 years</SelectItem>
                    <SelectItem value="3-5 years">3-5 years</SelectItem>
                    <SelectItem value="5+ years">5+ years</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Switch
                  id="remote"
                  checked={filters.remote}
                  onCheckedChange={(checked) => handleFilterChange('remote', checked)}
                />
                <label htmlFor="remote" className="text-sm font-medium text-gray-700">
                  Remote only
                </label>
              </div>
              <Button 
                variant="outline" 
                onClick={() => setFilters({
                  types: [],
                  locations: [],
                  experience: "",
                  remote: false,
                })}
                className="text-black border-gray-300 hover:bg-gray-100"
              >
                Clear Filters
              </Button>
            </div>
          </div>
        </div>

        {/* Feed */}
        <div className="max-w-7xl mx-auto mt-8 px-4 sm:px-6 lg:px-8">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 rounded-lg bg-purple-100 p-1">
              <TabsTrigger 
                value="recent" 
                className="rounded-md py-2.5 text-sm font-medium leading-5 text-purple-700 ring-white ring-opacity-60 ring-offset-2 ring-offset-purple-400 focus:outline-none focus:ring-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
              >
                Recent
              </TabsTrigger>
              <TabsTrigger 
                value="saved"
                className="rounded-md py-2.5 text-sm font-medium leading-5 text-purple-700 ring-white ring-opacity-60 ring-offset-2 ring-offset-purple-400 focus:outline-none focus:ring-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
              >
                Saved
              </TabsTrigger>
              <TabsTrigger 
                value="applied"
                className="rounded-md py-2.5 text-sm font-medium leading-5 text-purple-700 ring-white ring-opacity-60 ring-offset-2 ring-offset-purple-400 focus:outline-none focus:ring-2 data-[state=active]:bg-white data-[state=active]:shadow-sm"
              >
                Applied
              </TabsTrigger>
            </TabsList>
            <TabsContent value={activeTab} className="mt-6 space-y-6">
              {displayedOpportunities.map((opp) => (
                <Card key={opp.id} className="overflow-hidden transition-shadow duration-300 hover:shadow-lg">
                  <CardHeader className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
                    <CardTitle className="text-xl">{opp.title}</CardTitle>
                    <p className="text-purple-100">{opp.company} • {opp.location} • ${opp.salary}k/year</p>
                  </CardHeader>
                  <CardContent className="pt-4">
                    <p className="text-gray-700 mb-4">{opp.description}</p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="secondary" className="bg-purple-100 text-purple-800">{opp.type}</Badge>
                      <Badge variant="secondary" className="bg-indigo-100 text-indigo-800">{opp.experience}</Badge>
                      {opp.tags.map((tag) => (
                        <Badge key={tag} variant="outline" className="text-gray-700">{tag}</Badge>
                      ))}
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between bg-gray-50">
                    <Button 
                      variant="outline" 
                      size="sm"
                      className="text-black border-gray-300 hover:bg-gray-100"
                    >
                      Learn More
                    </Button>
                    <div className="flex space-x-2">
                      <Button 
                        variant={opp.saved ? "default" : "ghost"} 
                        size="icon"
                        onClick={() => handleSave(opp.id)}
                        className={opp.saved ? "bg-purple-600 text-white hover:bg-purple-700" : "text-purple-600 hover:text-purple-800 hover:bg-purple-100"}
                      >
                        <Bookmark className="h-4 w-4" />
                      </Button>
                      <Button 
                        onClick={() => handleApply(opp.id)}
                        disabled={opp.applied}
                        className={opp.applied ? "bg-green-600 text-white" : "bg-purple-600 text-white hover:bg-purple-700"}
                      >
                        {opp.applied ? "Applied" : "Apply Now"}
                      </Button>
                    </div>
                  </CardFooter>
                </Card>
              ))}
            </TabsContent>
          </Tabs>
        </div>
      </main>

      {/* Right Sidebar */}
      <aside className="w-80 bg-white shadow-lg p-6 hidden lg:block">
        <h2 className="text-lg font-semibold mb-4 text-purple-700">Notifications</h2>
        <ul className="space-y-4">
          <li className="flex items-center space-x-3 bg-purple-50 p-3 rounded-lg">
            <span className="w-2 h-2 bg-purple-500 rounded-full" />
            <span className="text-sm text-gray-700">New internship opportunity at Google</span>
          </li>
          <li className="flex items-center space-x-3 bg-purple-50 p-3 rounded-lg">
            <span className="w-2 h-2 bg-purple-500 rounded-full" />
            <span className="text-sm text-gray-700">Your application was viewed by Amazon</span>
          </li>
        </ul>
        <h2 className="text-lg font-semibold mt-8 mb-4 text-purple-700">Suggested Connections</h2>
        <ul className="space-y-4">
          <li className="flex items-center space-x-3 bg-indigo-50 p-3 rounded-lg">
            <Avatar>
              <AvatarImage src="/placeholder.svg?height=32&width=32" alt="Jane Doe" />
              <AvatarFallback>JD</AvatarFallback>
            </Avatar>
            <div>
              <p className="text-sm font-medium text-gray-700">Jane Doe</p>
              <p className="text-xs text-gray-500">Computer Science Student</p>
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              className="ml-auto text-black border-gray-300 hover:bg-gray-100"
            >
              Connect
            </Button>
          </li>
          <li className="flex items-center space-x-3 bg-indigo-50 p-3 rounded-lg">
            <Avatar>
              <AvatarImage src="/placeholder.svg?height=32&width=32" alt="John Smith" />
              <AvatarFallback>JS</AvatarFallback>
            </Avatar>
            <div>
              <p className="text-sm font-medium text-gray-700">John Smith</p>
              <p className="text-xs text-gray-500">Data Science Enthusiast</p>
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              className="ml-auto text-black border-gray-300 hover:bg-gray-100"
            >
              Connect
            </Button>
          </li>
        </ul>
      </aside>
    </div>
  )
}